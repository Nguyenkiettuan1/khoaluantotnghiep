import pandas as pd
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import spacy


# Hàm chia câu bằng spaCy (thay cho sent_tokenize của NLTK)
def sent_tokenize_spacy(text: str) -> list:
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]

# Load file kết quả
df = pd.read_excel("evaluation_results.xlsx")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Ngưỡng
THRESHOLD = 0.7
COVER_THRESHOLD = 0.75

# Hàm đánh giá theo từng phần câu (semantic partial overlap)
def semantic_overlap_partial_match(candidate: str, reference: str, threshold=THRESHOLD) -> float:
    ref_clauses = sent_tokenize_spacy(str(reference))  # Dùng spaCy
    if not ref_clauses:
        return 0.0

    cand_emb = model.encode(candidate, convert_to_tensor=True)
    matched = 0

    for clause in ref_clauses:
        clause_emb = model.encode(clause, convert_to_tensor=True)
        score = util.cos_sim(clause_emb, cand_emb).item()
        if score >= threshold:
            matched += 1

    return matched / len(ref_clauses)

# Đánh giá recall từng mô hình
df["Recall_DeepSeek"] = df.apply(lambda r: semantic_overlap_partial_match(r["Câu trả lời DeepSeek"], r["Đáp án chuẩn"]), axis=1)
df["Recall_Gemini"]   = df.apply(lambda r: semantic_overlap_partial_match(r["Câu trả lời Gemini"], r["Đáp án chuẩn"]), axis=1)
df["Recall_OpenAI"]   = df.apply(lambda r: semantic_overlap_partial_match(r["Câu trả lời OpenAI"], r["Đáp án chuẩn"]), axis=1)

# Đánh nhãn 1 nếu đạt đủ độ phủ nội dung
df["Pred_DeepSeek"] = (df["Recall_DeepSeek"] >= COVER_THRESHOLD).astype(int)
df["Pred_Gemini"]   = (df["Recall_Gemini"] >= COVER_THRESHOLD).astype(int)
df["Pred_OpenAI"]   = (df["Recall_OpenAI"] >= COVER_THRESHOLD).astype(int)
df["TrueLabel"] = 1

# Tính precision, recall, f1, accuracy
metrics = []
for model in ["DeepSeek", "Gemini", "OpenAI"]:
    y_pred = df[f"Pred_{model}"]
    metrics.append({
        "Mô hình": model,
        "Precision": precision_score(df["TrueLabel"], y_pred, zero_division=0),
        "Recall": recall_score(df["TrueLabel"], y_pred, zero_division=0),
        "F1-score": f1_score(df["TrueLabel"], y_pred, zero_division=0),
        "Accuracy": accuracy_score(df["TrueLabel"], y_pred)
    })

# Xuất file kết quả
df_metrics = pd.DataFrame(metrics)
df_metrics.to_excel("semantic_partial_overlap_scores.xlsx", index=False)
print("✅ Đã lưu kết quả vào semantic_partial_overlap_scores.xlsx")
