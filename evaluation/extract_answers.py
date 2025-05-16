import os
import pandas as pd
import asyncio
from openai import OpenAI
from dotenv import load_dotenv
import sys

# === Load cấu hình ===
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import get_answer_from_search_results, extract_labels_from_file
from neo4jconnector import Neo4jConnection

def init_client(dbname: str) -> Neo4jConnection:
    return Neo4jConnection(
        uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        user=os.getenv("NEO4J_USER", "neo4j"),
        password=os.getenv("NEO4J_PASSWORD"),
        dbname=dbname
    )

# === Async gọi mô hình trả lời ===
async def evaluate_question_async(question: str) -> dict:
    async def fetch(client, labels):
        return await asyncio.to_thread(get_answer_from_search_results, client, question, labels)

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

async def main_async():
    df_input = pd.read_csv("./evaluation/sgu_golden_answers_updated.csv")
    results = []
    for _, row in df_input.iterrows():
        res = await evaluate_question_async(row["Câu hỏi"])
        res["Đáp án chuẩn"] = row["Đáp án chuẩn"]
        results.append(res)
    df = pd.DataFrame(results)
    df.to_excel("evaluation_answers_only.xlsx", index=False)
    print("✅ Đã lưu câu trả lời vào file evaluation_answers_only.xlsx")

# === Khởi tạo kết nối ===
client_deepseek = init_client("deepseek")
client_gemini   = init_client("gemini")
client_openai   = init_client("openai")
labels_deepseek = extract_labels_from_file("labels/neo4j_labels_deepseek.txt")
labels_gemini   = extract_labels_from_file("labels/neo4j_labels_gemini.txt")
labels_openai   = extract_labels_from_file("labels/neo4j_labels_openai.txt")

if __name__ == "__main__":
    asyncio.run(main_async())

