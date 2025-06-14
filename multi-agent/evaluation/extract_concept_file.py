import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv
import re

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load file CQ và Đáp án chuẩn
df = pd.read_csv("sgu_golden_answers_updated.csv")

# Hàm trích xuất concept từ đáp án chuẩn
def extract_concepts(text: str) -> list:
    prompt = f"""
Đoạn sau là một câu trả lời từ hệ thống:
{text}

Hãy liệt kê các khái niệm (concept) quan trọng nhất cần có để tạo ontology từ câu trả lời trên. 
Chỉ trả về danh sách dạng gạch đầu dòng, mỗi dòng là một khái niệm, không giải thích thêm.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=200
        )
        output = response.choices[0].message.content
        lines = [re.sub(r"^[-•\\d\\.\\)]\\s*", "", line.strip()) for line in output.splitlines() if line.strip()]
        return list(filter(None, lines))
    except:
        return []

# Tạo bảng concept cho mỗi mô hình
concept_entries = []
models = ["DeepSeek", "Gemini", "OpenAI"]

for _, row in df.iterrows():
    question = row["Câu hỏi"]
    gold_answer = row["Đáp án chuẩn"]
    concepts = extract_concepts(gold_answer)
    for model in models:
        for concept in concepts:
            concept_entries.append({
                "Câu hỏi": question,
                "Mô hình": model,
                "Concept": concept
            })

concept_df = pd.DataFrame(concept_entries)
concept_df.to_excel("evaluation_kg_concepts.xlsx", index=False)
concept_df.head()
