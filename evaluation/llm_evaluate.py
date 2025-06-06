import pandas as pd
import re
import os
import matplotlib.pyplot as plt
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === Chấm điểm câu trả lời CQ ===
def gpt_score(reference: str, candidate: str) -> int:
    prompt = f"""
[Gold Answer]: {reference}
[Model Answer]: {candidate}

Đánh giá mức độ khớp giữa [Model Answer] và [Gold Answer] trên thang điểm từ 0 đến 10.
0 = hoàn toàn không đúng, 10 = khớp hoàn toàn.
Chỉ trả về một số nguyên trong khoảng 0–10.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-o4-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=10
        )
        score_text = response.choices[0].message.content.strip()
        return int(re.search(r"\d+", score_text).group())
    except:
        return 0

# === Gán nhãn từ điểm ===
def classify_label(score: int) -> str:
    if score >= 6:
        return "Right"
    elif score < 3:
        return "Wrong"
    else:
        return "Partial"

# === Kiểm tra concept có xuất hiện trong câu trả lời không ===
def gpt_concept_check(concept: str, answer: str) -> int:
    prompt = f"""
[Concept]: {concept}
[Answer]: {answer}

Khái niệm [Concept] có được đề cập rõ ràng hoặc ngụ ý trong [Answer] không?
Chỉ trả lời: yes hoặc no.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-o4-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=10
        )
        return 1 if "yes" in response.choices[0].message.content.strip().lower() else 0
    except:
        return 0

# === Đánh giá tổng thể từ file chứa câu trả lời + concept ===
def evaluate_from_file(file_path: str, concept_file: str):
    df = pd.read_excel(file_path)
    df_concept = pd.read_excel(concept_file)  # file gồm: Câu hỏi, Mô hình, Concept
    models = ["DeepSeek", "Gemini", "OpenAI"]

    for model in models:
        df[f"Score_{model}"] = df.apply(lambda r: gpt_score(r["Đáp án chuẩn"], r[f"Câu trả lời {model}"]), axis=1)
        df[f"Label_{model}"] = df[f"Score_{model}"].apply(classify_label)

    # Đánh giá concept khớp
    results = []
    for _, row in df_concept.iterrows():
        question = row["Câu hỏi"]
        concept = row["Concept"]
        model = row["Mô hình"]
        matched_row = df[df["Câu hỏi"] == question]
        if not matched_row.empty:
            answer = matched_row.iloc[0][f"Câu trả lời {model}"]
            ok = gpt_concept_check(concept, answer)
            results.append({"Câu hỏi": question, "Concept": concept, "Mô hình": model, "Khớp": ok})

    pd.DataFrame(results).to_excel("evaluation_concepts_result.xlsx", index=False)
    df.to_excel("evaluation_labels_only.xlsx", index=False)
    print("✅ Đánh giá hoàn tất (câu trả lời + concept) đúng theo bài báo.")

if __name__ == "__main__":
    evaluate_from_file("evaluation_answers_only.xlsx", "evaluation_kg_concepts.xlsx")
    
