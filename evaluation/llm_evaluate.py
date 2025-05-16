# import sys, os
# import pandas as pd
# import re
# import asyncio
# import time
# from typing import List
# from openai import OpenAI
# from dotenv import load_dotenv
# from scipy.spatial.distance import cosine
# from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
# import matplotlib.pyplot as plt
# from sklearn.metrics import roc_curve, auc

# # === Cấu hình ===
# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# from app import get_answer_from_search_results, extract_labels_from_file
# from neo4jconnector import Neo4jConnection

# # === Hàm tiện ích ===
# def init_client(dbname: str) -> Neo4jConnection:
#     return Neo4jConnection(
#         uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
#         user=os.getenv("NEO4J_USER", "neo4j"),
#         password=os.getenv("NEO4J_PASSWORD"),
#         dbname=dbname
#     )

# # === Embedding API từ OpenAI ===
# def get_openai_embedding(text: str, model="text-embedding-ada-002"):
#     response = client.embeddings.create(model=model, input=text)
#     return response.data[0].embedding

# def compute_similarity_openai(text1: str, text2: str) -> float:
#     emb1 = get_openai_embedding(text1)
#     emb2 = get_openai_embedding(text2)
#     return 1 - cosine(emb1, emb2)

# # === GPT judge (Sllm) ===
# def gpt_judge(reference: str, candidate: str) -> int:
#     prompt = f"""
# [Gold Answer]: {reference}

# [Model Answer]: {candidate}

# Câu trả lời của [Model Answer] có mang theo ý nghĩa của ý nghĩa của câu trả lời chuẩn  ?
# Respond only with "yes" or "no"
# """
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0,
#             max_tokens=1000
#         )
#         answer = response.choices[0].message.content.strip().lower()
#         return 1 if "yes" in answer else 0
#     except Exception:
#         return 0

# # compute optimal threshold by Youden's J

# def optimal_threshold(y_true, y_score):
#     fpr, tpr, thresholds = roc_curve(y_true, y_score)
#     j_scores = tpr - fpr
#     idx = j_scores.argmax()
#     return thresholds[idx], fpr[idx], tpr[idx]

# # === Gọi từng mô hình tìm câu trả lời ===
# async def evaluate_question_async(question: str) -> dict:
#     async def fetch(client, labels):
#         return await asyncio.to_thread(get_answer_from_search_results, client, question, labels)

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

# # === Luồng chính ===
# async def main_async():
#     # Đọc input
#     df_input = pd.read_csv("./evaluation/sgu_golden_answers_updated.csv")
#     results = []
#     for _, row in df_input.iterrows():
#         res = await evaluate_question_async(row["Câu hỏi"])
#         res["Đáp án chuẩn"] = row["Đáp án chuẩn"]
#         results.append(res)
#     df = pd.DataFrame(results)

#     # Tính similarity và judge
#     for model in ["DeepSeek", "Gemini", "OpenAI"]:
#         df[f"Sir_{model}"] = df.apply(lambda r: compute_similarity_openai(r["Đáp án chuẩn"], r[f"Câu trả lời {model}"]), axis=1)
#         time.sleep(1)
#         df[f"Sllm_{model}"] = df.apply(lambda r: gpt_judge(r["Đáp án chuẩn"], r[f"Câu trả lời {model}"]), axis=1)

#     # Xác định threshold tối ưu và vẽ ROC
#     thresholds_info = {}
#     for model in ["DeepSeek", "Gemini", "OpenAI"]:
#         y_true  = df[f"Sllm_{model}"]
#         y_score = df[f"Sir_{model}"]
#         thr, fpr_opt, tpr_opt = optimal_threshold(y_true, y_score)
#         thresholds_info[model] = thr

#         # Vẽ ROC
#         fpr, tpr, _ = roc_curve(y_true, y_score)
#         roc_auc = auc(fpr, tpr)
#         plt.figure(figsize=(6,6))
#         plt.plot(fpr, tpr, lw=2, label=f"{model} (AUC={roc_auc:.2f})")
#         plt.plot([0,1], [0,1], linestyle='--', color='gray')
#         plt.scatter(fpr_opt, tpr_opt, marker='o', color='red', label=f"Opt Thr={thr:.2f}")
#         plt.xlabel('False Positive Rate')
#         plt.ylabel('True Positive Rate')
#         plt.title(f'ROC Curve - {model}')
#         plt.legend(loc='lower right')
#         plt.tight_layout()
#         plt.savefig(f"roc_curve_{model.lower()}.png")
#         plt.close()

#     # Áp threshold tối ưu để tính match
#     for model in ["DeepSeek", "Gemini", "OpenAI"]:
#         thr = thresholds_info[model]
#         df[f"Match_{model}"] = df.apply(lambda r: int(r[f"Sir_{model}"] >= thr and r[f"Sllm_{model}"]==1), axis=1)

#     # Tính metrics
#     metrics = []
#     for model in ["DeepSeek", "Gemini", "OpenAI"]:
#         y_true = df[f"Sllm_{model}"]
#         y_pred = df[f"Match_{model}"]
#         metrics.append({
#             "Model": model,
#             "Precision": precision_score(y_true, y_pred),
#             "Recall": recall_score(y_true, y_pred),
#             "F1": f1_score(y_true, y_pred),
#             "Accuracy": accuracy_score(y_true, y_pred),
#             "Threshold": thresholds_info[model]
#         })
#     df_metrics = pd.DataFrame(metrics)

#     # Lưu kết quả
#     df.to_excel("evaluation_results_with_scores.xlsx", index=False)
#     df_metrics.to_excel("llms4om_metrics.xlsx", index=False)
#     print("✅ Đã lưu kết quả và ROC curves.")

# # Khởi tạo kết nối
# client_deepseek = init_client("deepseek")
# client_gemini   = init_client("gemini")
# client_openai   = init_client("openai")
# labels_deepseek = extract_labels_from_file("labels/neo4j_labels_deepseek.txt")
# labels_gemini   = extract_labels_from_file("labels/neo4j_labels_gemini.txt")
# labels_openai   = extract_labels_from_file("labels/neo4j_labels_openai.txt")

# if __name__ == "__main__":
#     asyncio.run(main_async())





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
            model="gpt-4o-mini",
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
            model="gpt-4o-mini",
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
    
