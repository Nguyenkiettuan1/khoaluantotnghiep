# import sys, os
# import pandas as pd
# import re
# from typing import List
# import asyncio
# from openai import OpenAI

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from app import get_answer_from_search_results, extract_labels_from_file
# from neo4jconnector import Neo4jConnection

# def clean_question_line(line: str) -> str:
#     return re.sub(r"^\d+\.\s*", "", line).strip()

# def read_questions_from_file(filepath: str) -> List[str]:
#     with open(filepath, 'r', encoding='utf-8') as file:
#         return [clean_question_line(line) for line in file if line.strip()]

# def init_client(dbname: str) -> Neo4jConnection:
#     return Neo4jConnection(
#         uri=os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
#         user=os.getenv('NEO4J_USER', 'neo4j'),
#         password=os.getenv('NEO4J_PASSWORD'),
#         dbname=dbname
#     )

# # Gọi 3 client đồng thời cho 1 câu hỏi
# async def evaluate_question_async(question: str) -> dict:
#     async def fetch(client, labels):
#         try:
#             return await asyncio.to_thread(get_answer_from_search_results, client, question, labels)
#         except Exception as e:
#             return f"[ERROR] {e}"

#     # Chạy song song 3 client
#     deepseek_task = fetch(client_deepseek, labels_deepseek)
#     gemini_task = fetch(client_gemini, labels_gemini)
#     openai_task = fetch(client_openai, labels_openai)

#     deepseek_ans, gemini_ans, openai_ans = await asyncio.gather(
#         deepseek_task, gemini_task, openai_task
#     )

#     return {
#         "Câu hỏi": question,
#         "Câu trả lời DeepSeek": deepseek_ans,
#         "Câu trả lời Gemini": gemini_ans,
#         "Câu trả lời OpenAI": openai_ans
#     }

# async def main_async():
#     print("📥 Đang đọc câu hỏi...")
#     questions = read_questions_from_file("Qc/CQ_SGU.txt")
#     print(f"📌 Tổng cộng {len(questions)} câu hỏi.\n")

#     results = []

#     for i, question in enumerate(questions, 1):
#         print(f"[{i}/{len(questions)}] ✍️ {question}")
#         result = await evaluate_question_async(question)
#         results.append(result)

#     print("\n💾 Lưu kết quả vào file Excel...")
#     df = pd.DataFrame(results)
#     df.to_excel("evaluation_results.xlsx", index=False)
#     print("✅ Đã hoàn thành: evaluation_results.xlsx")

# # Khởi tạo client/labals toàn cục trước khi gọi async
# print("🔌 Kết nối database...")
# client_deepseek = init_client("deepseek")
# client_gemini = init_client("gemini")
# client_openai = init_client("openai")

# labels_deepseek = extract_labels_from_file("labels/neo4j_labels_deepseek.txt")
# labels_gemini = extract_labels_from_file("labels/neo4j_labels_gemini.txt")
# labels_openai = extract_labels_from_file("labels/neo4j_labels_openai.txt")

# # Chạy main async
# if __name__ == "__main__":
#     asyncio.run(main_async())




import sys, os
import pandas as pd
import re
import asyncio
import time
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from scipy.spatial.distance import cosine
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score


# === Cấu hình ===
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import get_answer_from_search_results, extract_labels_from_file
from neo4jconnector import Neo4jConnection

# === Hàm tiện ích ===
def init_client(dbname: str) -> Neo4jConnection:
    return Neo4jConnection(
        uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        user=os.getenv("NEO4J_USER", "neo4j"),
        password=os.getenv("NEO4J_PASSWORD"),
        dbname=dbname
    )

# === Embedding API từ OpenAI ===
def get_openai_embedding(text: str, model="text-embedding-ada-002"):
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding

def compute_similarity_openai(text1: str, text2: str) -> float:
    emb1 = get_openai_embedding(text1)
    emb2 = get_openai_embedding(text2)
    return 1 - cosine(emb1, emb2)

# === GPT judge (Sllm) ===
def gpt_judge(reference: str, candidate: str) -> int:
    prompt = f"""
[Gold Answer]: {reference}

[Model Answer]: {candidate}

Câu trả lời của [Model Answer] có mang theo ý nghĩa của ý nghĩa của câu trả lời chuẩn  ?
Respond only with "yes" or "no"
"""
    print(f"candidate: {candidate}")
    print(f"reference: {reference}")
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=1000
        )
        answer = response.choices[0].message.content.strip().lower()
        print(f"GPT Judge: {answer}")
        return 1 if "yes" in answer else 0
    except Exception as e:
        return 0  # hoặc ghi lỗi ra log

def is_match(sir: float, sllm: int, threshold=0.6) -> int:
    return int(sir >= threshold and sllm == 1)

# === Gọi từng mô hình tìm câu trả lời ===
async def evaluate_question_async(question: str) -> dict:
    async def fetch(client, labels):
        try:
            return await asyncio.to_thread(get_answer_from_search_results, client, question, labels)
        except Exception as e:
            return f"[ERROR] {e}"

    deepseek_task = fetch(client_deepseek, labels_deepseek)
    gemini_task = fetch(client_gemini, labels_gemini)
    openai_task = fetch(client_openai, labels_openai)

    deepseek_ans, gemini_ans, openai_ans = await asyncio.gather(
        deepseek_task, gemini_task, openai_task
    )

    return {
        "Câu hỏi": question,
        "Câu trả lời DeepSeek": deepseek_ans,
        "Câu trả lời Gemini": gemini_ans,
        "Câu trả lời OpenAI": openai_ans
    }

# === Luồng chính ===
async def main_async():
    print("📥 Đọc dữ liệu câu hỏi và đáp án chuẩn...")
    df_input = pd.read_csv("./evaluation/sgu_golden_answers_updated.csv")  # 2 cột: Câu hỏi, Đáp án chuẩn
    print(f"📌 Tổng cộng {len(df_input)} câu hỏi.\n")

    results = []
    for i, row in df_input.iterrows():
        print(f"[{i+1}/{len(df_input)}] ✍️ {row['Câu hỏi']}")
        result = await evaluate_question_async(row["Câu hỏi"])
        result["Đáp án chuẩn"] = row["Đáp án chuẩn"]
        results.append(result)

    df = pd.DataFrame(results)

    # === Đánh giá từng mô hình
    for model in ["DeepSeek", "Gemini", "OpenAI"]:
        print(f"🔍 Đánh giá mô hình {model}...")
        df[f"Sir_{model}"] = df.apply(lambda r: compute_similarity_openai(r["Đáp án chuẩn"], r[f"Câu trả lời {model}"]), axis=1)
        time.sleep(1)
        df[f"Sllm_{model}"] = df.apply(lambda r: gpt_judge(r["Đáp án chuẩn"], r[f"Câu trả lời {model}"]), axis=1)
        time.sleep(1)
        df[f"Match_{model}"] = df.apply(lambda r: is_match(r[f"Sir_{model}"], r[f"Sllm_{model}"]), axis=1)

    # === Tính chỉ số Precision/Recall/F1
    metrics = []
    for model in ["DeepSeek", "Gemini", "OpenAI"]:
        y_true = [1] * len(df)
        y_pred = df[f"Match_{model}"]
        metrics.append({
        "Model": model,
        "Precision": precision_score(y_true, y_pred),
        "Recall": recall_score(y_true, y_pred),
        "F1": f1_score(y_true, y_pred),
        "Accuracy": accuracy_score(y_true, y_pred)
        })

    df_metrics = pd.DataFrame(metrics)
    df.to_excel("evaluation_results_with_scores.xlsx", index=False)
    df_metrics.to_excel("llms4om_metrics.xlsx", index=False)
    print("✅ Đã lưu: evaluation_results_with_scores.xlsx và llms4om_metrics.xlsx")

# === Kết nối database
print("🔌 Khởi tạo kết nối Neo4j...")
client_deepseek = init_client("deepseek")
client_gemini = init_client("gemini")
client_openai = init_client("openai")

labels_deepseek = extract_labels_from_file("labels/neo4j_labels_deepseek.txt")
labels_gemini = extract_labels_from_file("labels/neo4j_labels_gemini.txt")
labels_openai = extract_labels_from_file("labels/neo4j_labels_openai.txt")

# === Chạy chính
if __name__ == "__main__":
    asyncio.run(main_async())