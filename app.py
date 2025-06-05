import streamlit as st
import os
import time
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
from collections import defaultdict, deque

import pandas as pd
from dotenv import load_dotenv
from neo4jconnector import Neo4jConnection, Neo4jVectorSearchError

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config("SGU Vector Chatbot", page_icon="🎓", layout="centered")


@dataclass
class SearchResult:
    name: str
    node_type: str
    similarity: float
    description: Optional[str] = None

# 1) Cache Neo4j clients -------------------------------------------------------
@st.cache_resource(show_spinner=False)
def init_neo4j_clients() -> Dict[str, Dict]:
    cfg = {
        "uri": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        "user": os.getenv("NEO4J_USER", "neo4j"),
        "password": os.getenv("NEO4J_PASSWORD"),
    }
    return {
        "deepseek": {
            "conn": Neo4jConnection(**cfg, dbname="deepseek"),
            "label_file": "labels/neo4j_labels_deepseek.txt",
        },
        "gemini": {
            "conn": Neo4jConnection(**cfg, dbname="gemini"),
            "label_file": "labels/neo4j_labels_gemini.txt",
        },
        "openai": {
            "conn": Neo4jConnection(**cfg, dbname="openai"),
            "label_file": "labels/neo4j_labels_openai.txt",
        },
    }

# 2) Cache Graph & Direct Map --------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_relation_graph(client_name: str) -> Dict[str, List[tuple]]:
    path_map = {
        "deepseek": "ontology_relations_deepseek.csv",
        "gemini":   "ontology_relations_gemini.csv",
        "openai":   "ontology_relations_openai.csv"
    }
    path = path_map.get(client_name)
    if not path or not os.path.exists(path):
        return {}
    df = pd.read_csv(path)
    graph = defaultdict(list)
    for rel in df.to_dict(orient="records"):
        subj = rel["subject"].split("#")[-1].replace("_", " ").strip()
        obj  = rel["object"].split("#")[-1].replace("_", " ").strip()
        pred = rel["predicate"].split("#")[-1].strip()
        graph[subj].append((obj, pred))
    return graph

@st.cache_resource(show_spinner=False)
def load_direct_map(client_name: str) -> Dict[str, List[Dict]]:
    path = f"./precomputed_relations/{client_name}_direct_map.json"
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as fp:
        return json.load(fp)

# 3) Các hàm hỗ trợ (vector search, load labels, load ontology triples) ----------
def perform_search(neo4j: Neo4jConnection, query: str, node_types: List[str],
                   min_similarity: float = 0.5, limit: int = 15) -> List[Dict]:
    all_results = []
    try:
        for node_type in node_types:
            results = neo4j.similarity_search(
                query_text=query,
                node_label=node_type,
                limit=limit,
                min_similarity=min_similarity
            )
            for r in results:
                r['node_type'] = node_type
            all_results.extend(results)
    except Exception as e:
        st.error(f"Error performing search: {str(e)}")
    return sorted(all_results, key=lambda x: x['similarity'], reverse=True)

def load_labels(path: str) -> List[str]:
    with open(path, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]

 

def find_indirect_paths(graph: Dict, start: str, targets: set, max_depth: int = 3):
    """Nếu vẫn cần hàm này cho BFS riêng lẻ."""
    paths = []
    queue = deque([(start, [], {start})])
    while queue:
        node, path, visited = queue.popleft()
        if len(path) > max_depth:
            continue
        for neighbor, rel in graph.get(node, []):
            if neighbor in visited:
                continue
            new_path = path + [(node, rel, neighbor)]
            if neighbor in targets:
                paths.append(new_path)
            else:
                queue.append((neighbor, new_path, visited | {neighbor}))
    return paths

# 4) Hàm xử lý query từng lần user submit -------------------------------------
def handle_query(
    prompt: str,
    neo4j: Neo4jConnection,
    labels: List[str],
    graph: Dict[str, List[tuple]],
    direct_map: Dict[str, List[Dict]],
    min_sim: float = 0.5,
    limit: int = 15
):
    # 4.1) Lưu lịch sử và hiển thị user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 4.2) Vector search
    with st.spinner("🔎 Đang tìm kiếm..."):
        results = perform_search(neo4j, prompt, labels, min_similarity=min_sim, limit=limit)
        st.session_state.last_results = results

    if not results:
        response_text = "Không tìm thấy kết quả phù hợp."
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        return

    # 4.3) Chuẩn bị related_relations
    names = set(r["name"] for r in results)
    related_relations = []

    # 4.3a) Direct lookup từ direct_map (precomputed)
    for name in names:
        for pair in direct_map.get(name, []):
            subj = name
            pred = pair["predicate"]
            obj  = pair["neighbor"]
            related_relations.append(f"{subj} → {pred} → {obj}")

    # 4.3b) Nếu chưa tìm được direct, chạy multi-source BFS
    if not related_relations:
        top_names = sorted(
            names,
            key=lambda n: next((r["similarity"] for r in results if r["name"] == n), 0),
            reverse=True
        )[:5]
        targets = set(top_names)
        coverage_target = 0.7
        max_depth_cap   = 3
        covered         = set()
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

    # 4.4) Generate answer với GPT/Gemini
    with st.chat_message("assistant"):
        with st.spinner("🤖 Trợ lý đang trả lời..."):
            chat_history_copy = st.session_state.chat_history.copy()
            response_text = neo4j.generate_answer(
                prompt,
                results,
                ontology_relations=related_relations,
                chat_history=chat_history_copy
            )
            st.markdown(response_text)
    st.session_state.chat_history.append({"role": "assistant", "content": response_text})

    # 4.5) Hiển thị chi tiết kết quả
    with st.expander("🔎 Chi tiết kết quả"):
        for r in results:
            st.markdown(
                f"**{r['name']}** ({r['node_type']}) — Similarity: `{r['similarity']:.4f}`"
            )
            if desc := r.get("description"):
                st.write(desc)
            st.divider()

# 5) Hàm main ---------------------------------------------------------------
def main():
    st.title("🎓 Trợ lý Chatbot SGU")

    # Khởi tạo state lần đầu
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "last_results" not in st.session_state:
        st.session_state.last_results = []

    # 5.1) Load/cached resources (chỉ chạy 1 lần mỗi khi client_name thay đổi)
    clients = init_neo4j_clients()
    client_name = st.sidebar.selectbox("🔧 Chọn mô hình", list(clients))
    neo4j = clients[client_name]["conn"]
    labels = load_labels(clients[client_name]["label_file"])
    graph = get_relation_graph(client_name)
    direct_map = load_direct_map(client_name)


    # 5.3) Hiển thị lịch sử chat
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 5.4) Nhận input user
    prompt = st.chat_input("Nhập câu hỏi...")

    if prompt:
        handle_query(
            prompt=prompt,
            neo4j=neo4j,
            labels=labels,
            graph=graph,
            direct_map=direct_map,
        )

    # 5.5) Nút xóa lịch sử
    if st.sidebar.button("🧹 Xóa hội thoại"):
        st.session_state.chat_history = []
        st.session_state.last_results = []
        st.experimental_rerun()

if __name__ == "__main__":
    main()
