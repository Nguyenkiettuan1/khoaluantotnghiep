import os
import sys
import time
import asyncio
import pandas as pd
from typing import List, Dict, Optional
from collections import deque
from dotenv import load_dotenv
from openai import OpenAI

# Đảm bảo project path để import module app và neo4jconnector
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from neo4jconnector import Neo4jConnection
from app import get_relation_graph, load_direct_map

# === Load cấu hình môi trường ===
load_dotenv()
_ = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === Hàm đọc labels từ file ===
def read_labels(label_path: str) -> List[str]:
    labels = []
    with open(label_path, "r", encoding="utf-8") as f:
        for line in f:
            txt = line.strip()
            if txt:
                labels.append(txt)
    return labels

# === Khởi tạo kết nối Neo4j cho DBname tương ứng ===
def init_neo4j_client(dbname: str) -> Neo4jConnection:
    return Neo4jConnection(
        uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        user=os.getenv("NEO4J_USER", "neo4j"),
        password=os.getenv("NEO4J_PASSWORD"),
        dbname=dbname
    )

# === Load ontology relations cho client cụ thể với logic BFS đầy đủ ===
def load_ontology_relations(client_name: str, search_results: List[Dict] = None) -> List[str]:
    """Load ontology relations từ graph và direct_map với BFS logic"""
    try:
        graph = get_relation_graph(client_name)
        direct_map = load_direct_map(client_name)
        
        # Nếu không có search_results, chỉ trả về direct relations
        if not search_results:
            relations = []
            for name, pairs in direct_map.items():
                for pair in pairs:
                    pred = pair["predicate"]
                    obj = pair["neighbor"]
                    relations.append(f"{name} → {pred} → {obj}")
            return relations
        
        # 4.3) Chuẩn bị related_relations với logic BFS
        names = set(r["name"] for r in search_results)
        related_relations = []

        # 4.3a) Direct lookup từ direct_map (precomputed)
        for name in names:
            for pair in direct_map.get(name, []):
                subj = name
                pred = pair["predicate"]
                obj = pair["neighbor"]
                related_relations.append(f"{subj} → {pred} → {obj}")

        # 4.3b) Nếu chưa tìm được direct, chạy multi-source BFS
        if not related_relations:
            top_names = sorted(
                names,
                key=lambda n: next((r["similarity"] for r in search_results if r["name"] == n), 0),
                reverse=True
            )[:5]
            targets = set(top_names)
            coverage_target = 0.7
            max_depth_cap = 3
            covered = set()
            queue = deque([(n, [(n, None)], {n}) for n in targets])
            depth_now = 0
            start_t = time.perf_counter()
            TIMEOUT = 0.15

            while queue and depth_now < max_depth_cap:
                qlen = len(queue)
                for _ in range(qlen):
                    if time.perf_counter() - start_t > TIMEOUT:
                        related_relations.append("⚠️ Cắt ngắn reasoning do timeout")
                        queue.clear()
                        break

                    node, path, visited = queue.popleft()
                    for neigh, rel in graph.get(node, []):
                        if neigh in visited:
                            continue
                        new_path = path + [(neigh, rel)]
                        if neigh in targets:
                            sentence = " → ".join([
                                f"{src} --{r}→ {dst}"
                                for (src, _), (dst, r) in zip(new_path, new_path[1:])
                            ])
                            related_relations.append(f"Đường vòng (depth {len(new_path)-1}): {sentence}")
                            covered.update({p[0] for p in new_path})
                        elif len(new_path)-1 < max_depth_cap:
                            queue.append((neigh, new_path, visited | {neigh}))
                depth_now += 1
                if covered and (len(covered) / len(targets) >= coverage_target):
                    break
        
        return related_relations
        
    except Exception as e:
        print(f"Warning: Could not load ontology relations for {client_name}: {e}")
        return []

# === Hàm trả lời bằng generate_answer_v1 + đo thời gian ===
def answer_v1_timed(client: Neo4jConnection, question: str, labels: List[str]) -> Dict[str, Optional[str]]:
    """
    Dùng generate_answer_v1 (chỉ dựa trên search_results), đo thời gian.
    """
    result = {"answer_v1": None, "time_v1": None}
    try:
        start = time.perf_counter()

        # 1) Vector-search
        search_results = []
        for node_type in labels:
            partial = client.similarity_search(
                query_text=question,
                node_label=node_type,
                limit=30,
                min_similarity=0.6
            )
            for r in partial:
                r["node_type"] = node_type
            search_results.extend(partial)
        search_results.sort(key=lambda x: x["similarity"], reverse=True)

        if not search_results:
            answer = "Không tìm thấy kết quả phù hợp."
        else:
            # Gọi generate_answer_v1 (không cần ontology)
            answer = client.generate_answer_v1(question, search_results)

        end = time.perf_counter()
        result["answer_v1"] = answer
        result["time_v1"] = end - start

    except Exception as e:
        result["answer_v1"] = f"Lỗi v1: {e}"
        result["time_v1"] = None

    return result

# === Hàm trả lời bằng generate_answer (có ontology) + đo thời gian ===
def answer_v2_timed(client: Neo4jConnection, question: str, labels: List[str], client_name: str) -> Dict[str, Optional[str]]:
    """
    Dùng generate_answer (dùng search_results + ontology_relations), đo thời gian.
    """
    result = {"answer_v2": None, "time_v2": None}
    try:
        start = time.perf_counter()

        # 1) Vector-search
        search_results = []
        for node_type in labels:
            partial = client.similarity_search(
                query_text=question,
                node_label=node_type,
                limit=30,
                min_similarity=0.6
            )
            for r in partial:
                r["node_type"] = node_type
            search_results.extend(partial)
        search_results.sort(key=lambda x: x["similarity"], reverse=True)

        if not search_results:
            answer = "Không tìm thấy kết quả phù hợp."
        else:
            # Load ontology relations với search_results để chạy BFS
            ontology_relations = load_ontology_relations(client_name, search_results)
            answer = client.generate_answer(
                question,
                search_results,
                ontology_relations=ontology_relations,
            )

        end = time.perf_counter()
        result["answer_v2"] = answer
        result["time_v2"] = end - start

    except Exception as e:
        result["answer_v2"] = f"Lỗi v2: {e}"
        result["time_v2"] = None

    return result

# === Async wrapper để chạy song song ba client và hai phiên bản v1/v2 ===
async def evaluate_question_async(question: str) -> Dict[str, object]:
    async def wrap(fn, *args):
        return await asyncio.to_thread(fn, *args)

    # Tạo tasks cho v1 và v2 trên từng client
    ds_v1 = wrap(answer_v1_timed, client_deepseek, question, labels_deepseek)
    ds_v2 = wrap(answer_v2_timed, client_deepseek, question, labels_deepseek, "deepseek")

    gm_v1 = wrap(answer_v1_timed, client_gemini, question, labels_gemini)
    gm_v2 = wrap(answer_v2_timed, client_gemini, question, labels_gemini, "gemini")

    oa_v1 = wrap(answer_v1_timed, client_openai, question, labels_openai)
    oa_v2 = wrap(answer_v2_timed, client_openai, question, labels_openai, "openai")

    # Chạy đồng thời 6 tác vụ
    ds1, ds2, gm1, gm2, oa1, oa2 = await asyncio.gather(
        ds_v1, ds_v2,
        gm_v1, gm_v2,
        oa_v1, oa_v2
    )

    return {
        "Câu hỏi": question,
        "Đáp án chuẩn": None,  # Sẽ được thêm vào sau trong main_async()
        # DeepSeek
        "Answer_v1 DeepSeek": ds1["answer_v1"],
        "Time_v1 DeepSeek (s)": ds1["time_v1"],
        "Answer_v2 DeepSeek": ds2["answer_v2"],
        "Time_v2 DeepSeek (s)": ds2["time_v2"],
        # Gemini
        "Answer_v1 Gemini": gm1["answer_v1"],
        "Time_v1 Gemini (s)": gm1["time_v1"],
        "Answer_v2 Gemini": gm2["answer_v2"],
        "Time_v2 Gemini (s)": gm2["time_v2"],
        # OpenAI
        "Answer_v1 OpenAI": oa1["answer_v1"],
        "Time_v1 OpenAI (s)": oa1["time_v1"],
        "Answer_v2 OpenAI": oa2["answer_v2"],
        "Time_v2 OpenAI (s)": oa2["time_v2"],
    }

# === Main async: đọc file đầu vào, đánh giá, lưu kết quả + timing summary ===
async def main_async():
    input_path = "./evaluation/sgu_golden_answers_updated.csv"
    if not os.path.exists(input_path):
        print(f"❌ Không tìm thấy file input: {input_path}")
        return

    df_input = pd.read_csv(input_path)
    records = []

    print(f"🚀 Bắt đầu đánh giá {len(df_input)} câu hỏi...")

    for i, row in df_input.iterrows():
        question_text = row["Câu hỏi"]
        golden_answer = row["Đáp án chuẩn"]
        
        print(f"⏳ Đang xử lý câu hỏi {i+1}/{len(df_input)}: {question_text[:50]}...")
        
        res = await evaluate_question_async(question_text)
        res["Đáp án chuẩn"] = golden_answer  # Thêm đáp án chuẩn vào kết quả
        records.append(res)

    df_results = pd.DataFrame(records)

    # Tính P50/P90 cho mỗi client và mỗi phiên bản
    summary = []
    time_columns = [
        "Time_v1 DeepSeek (s)", "Time_v2 DeepSeek (s)",
        "Time_v1 Gemini (s)", "Time_v2 Gemini (s)",
        "Time_v1 OpenAI (s)", "Time_v2 OpenAI (s)"
    ]
    
    for col in time_columns:
        if col in df_results.columns:
            times = df_results[col].dropna()
            if len(times) > 0:
                p50 = times.quantile(0.5)
                p90 = times.quantile(0.9)
                p99 = times.quantile(0.99)
                avg_time = times.mean()
                
                # Parse client name and version from column name
                parts = col.replace(" (s)", "").split(" ")
                version = parts[0].replace("Time_", "")
                client = " ".join(parts[1:])
                
                summary.append({
                    "Client": client,
                    "Version": version,
                    "Avg (s)": round(avg_time, 3),
                    "P50 (s)": round(p50, 3),
                    "P90 (s)": round(p90, 3),
                    "P99 (s)": round(p99, 3),
                    "Total Questions": len(times)
                })
    
    df_summary = pd.DataFrame(summary)

    # Xuất ra Excel với hai sheet: Answers và Timing Summary
    output_path = "evaluation_v1_v2_with_timing_complete.xlsx"
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_results.to_excel(writer, sheet_name="Answers", index=False)
        df_summary.to_excel(writer, sheet_name="Timing Summary", index=False)

    print(f"✅ Đã lưu kết quả hoàn chỉnh vào {output_path}")
    print(f"📊 Tổng cộng: {len(records)} câu hỏi đã được đánh giá")
    print(f"📈 Timing Summary:")
    print(df_summary.to_string(index=False))

# === Khởi tạo các client và labels trước khi chạy main ===
print("🔄 Đang khởi tạo kết nối Neo4j...")
client_deepseek = init_neo4j_client("deepseek")
client_gemini = init_neo4j_client("gemini")
client_openai = init_neo4j_client("openai")

print("📋 Đang load labels...")
labels_deepseek = read_labels("labels/neo4j_labels_deepseek.txt")
labels_gemini = read_labels("labels/neo4j_labels_gemini.txt")
labels_openai = read_labels("labels/neo4j_labels_openai.txt")

print("✅ Hoàn tất khởi tạo!")

if __name__ == "__main__":
    asyncio.run(main_async())