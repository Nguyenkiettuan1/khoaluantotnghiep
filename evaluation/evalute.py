from rdflib import Graph, Literal
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load mô hình embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load dữ liệu RDF
g_deepseek = Graph().parse("../ontology/cleaned_deepseek_v3_0324.ttl", format="turtle")
g_gemini = Graph().parse("../ontology/cleaned_gemini_flash_thinking.ttl", format="turtle")
g_openai = Graph().parse("../ontology/cleaned_openai_4o_mini.ttl", format="turtle")

# Câu hỏi và đáp án chuẩn
with open("../QC/CQ_SGU.txt", "r", encoding="utf-8") as f:
    questions = [line.strip() for line in f.readlines() if line.strip()]

answers_split = [
    "Trường Đại học Sài Gòn là cơ sở giáo dục đại học công lập trực thuộc Ủy ban Nhân dân TP. Hồ Chí Minh.",
    "Trường chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo.",
    "Trường đào tạo theo hai phương thức: chính quy và giáo dục thường xuyên (bao gồm vừa làm vừa học, văn bằng hai, liên thông).",
    "Trường có 05 chuyên ngành đào tạo tiến sĩ, 12 chuyên ngành cao học và 39 chương trình đào tạo trình độ đại học.",
    "Các lĩnh vực đào tạo chính bao gồm: Kinh tế, Kỹ thuật, Công nghệ, Văn hóa xã hội, Chính trị, Nghệ thuật và Sư phạm.",
    "Có. Trường được cấp Giấy chứng nhận kiểm định chất lượng giáo dục ngày 13/5/2017.",
    "Trường đào tạo 39 ngành trình độ đại học như: Giáo dục Chính trị, Du lịch, Mầm non, Kế toán, Tiểu học, Khoa học Môi trường, Âm nhạc, Kinh doanh Quốc tế, v.v.",
    "Chương trình chất lượng cao hiện tại là ngành Công nghệ Thông tin.",
    "Các ngành sau đại học gồm: Hóa hữu cơ, Hóa lý thuyết và Hóa lý, Khoa học Máy tính, Toán Giải tích, Lịch sử Việt Nam, Văn học Việt Nam, v.v.",
    "Trình độ tiến sĩ đào tạo các ngành: Hóa hữu cơ, Lịch sử Việt Nam, Quản lý Giáo dục, Toán Giải tích, Quản trị Kinh doanh.",
    "Giáo dục thường xuyên gồm: liên thông, vừa làm vừa học, bằng hai.",
    "Văn bằng hai gồm: Ngôn ngữ Anh, Kế toán, Luật, Quản trị Kinh doanh, Giáo dục Tiểu học và Quản lý Giáo dục.",
    "Có 3 cơ sở chính: 273 An Dương Vương (42.743m²), 105 Bà Huyện Thanh Quan (4.823m²), 04 Tôn Đức Thắng (19.655m²).",
    "Ký túc xá tại 99 An Dương Vương, Quận 8, diện tích 4.800m².",
    "Trường hợp tác với các quốc gia như Hoa Kỳ, Anh, Pháp, Nga, Singapore, Áo, Đài Loan, v.v.",
    "Chương trình Cử nhân Quốc tế liên kết với IMC Krems (Áo).",
    "Chương trình tiếng Hoa hợp tác với Trung tâm Hoa ngữ Sư phạm Đài Loan.",
    "Học bổng tiêu biểu: Bộ Y tế Singapore (Asian Nursing), Bộ Giáo dục Đài Loan.",
    "Liên kết đào tạo với Đại học Huddersfiled (Anh) ngành CNTT, TESOL, v.v.",
    "Điều kiện: học lực trung bình trở lên, không bị kỷ luật, không vi phạm quy định.",
    "Quyền lợi: được hỗ trợ kinh phí, cấp chứng nhận, cộng điểm rèn luyện, xét thưởng.",
    "Bài báo đăng tạp chí chuyên ngành hoặc kỷ yếu hội thảo đều được xét thưởng.",
    "Chi tiết NCKH xem tại Quy chế chương 7 hoặc hỏi giảng viên trợ lý NCKH.",
    "ISSN tạp chí: 1859-3208. Website: http://sj.sgu.edu.vn",
    "Phục vụ cán bộ, giảng viên, sinh viên các trường, viện, học viện.",
    "Tạp chí công bố kết quả nghiên cứu, bài giảng dạy - học tập.",
    "Nội dung: mục tiêu, kết quả mới, giá trị thực tiễn, phải được phản biện.",
    "Chuẩn trích dẫn: IEEE cho KHTN, APA cho KHXH và GD.",
    "Yêu cầu minh họa: 300dpi, định dạng JPG, PNG, BMP.",
    "Không phiên âm/dịch tên nước ngoài, phải nêu rõ nguồn và mã đề tài."
]

# Hàm đánh giá semantic (boolean)
def evaluate_semantic_match(graph, answers, threshold=0.6):
    result = []
    for answer in answers:
        embedding_answer = model.encode(answer, convert_to_tensor=True)
        found = False
        for s, p, o in graph:
            if isinstance(o, Literal):
                embedding_literal = model.encode(str(o), convert_to_tensor=True)
                score = float(util.cos_sim(embedding_answer, embedding_literal)[0][0])
                if score >= threshold:
                    found = True
                    break
        result.append(found)
    return result

# Hàm trích literal gần đúng nhất (cho hiển thị)
def evaluate_semantic_output(graph, answers, threshold=0.6):
    results = []
    for answer in answers:
        embedding_answer = model.encode(answer, convert_to_tensor=True)
        best_score = 0.0
        best_literal = ""
        for s, p, o in graph:
            if isinstance(o, Literal):
                embedding_literal = model.encode(str(o), convert_to_tensor=True)
                score = float(util.cos_sim(embedding_answer, embedding_literal)[0][0])
                if score > best_score:
                    best_score = score
                    best_literal = str(o)
        results.append(best_literal if best_score >= threshold else "")
    return results

# Tính chỉ số
def compute_metrics(y_pred):
    y_true = [True] * len(y_pred)
    return {
        "Accuracy": round(accuracy_score(y_true, y_pred), 3),
        "Precision": round(precision_score(y_true, y_pred, zero_division=0), 3),
        "Recall": round(recall_score(y_true, y_pred, zero_division=0), 3),
        "F1 Score": round(f1_score(y_true, y_pred, zero_division=0), 3)
    }

# Đánh giá Boolean
y_deepseek = evaluate_semantic_match(g_deepseek, answers_split)
y_gemini = evaluate_semantic_match(g_gemini, answers_split)
y_openai = evaluate_semantic_match(g_openai, answers_split)

# Bảng đánh giá tổng hợp
evaluation_df = pd.DataFrame({
    "DeepSeek": compute_metrics(y_deepseek),
    "Gemini": compute_metrics(y_gemini),
    "OpenAI": compute_metrics(y_openai)
}).T

print("\n--- Bảng đánh giá ---")
print(evaluation_df)

# Lưu bảng đánh giá chi tiết theo literal
matched_deepseek = evaluate_semantic_output(g_deepseek, answers_split)
matched_gemini = evaluate_semantic_output(g_gemini, answers_split)
matched_openai = evaluate_semantic_output(g_openai, answers_split)

df_matches = pd.DataFrame({
    "Câu hỏi": questions,
    "Đáp án chuẩn": answers_split,
    "DeepSeek trả lời": matched_deepseek,
    "Gemini trả lời": matched_gemini,
    "OpenAI trả lời": matched_openai
})


# Lưu các câu hỏi sai hoặc thiếu
wrong_df = pd.DataFrame({
    "Câu hỏi": questions,
    "DeepSeek đúng": y_deepseek,
    "Gemini đúng": y_gemini,
    "OpenAI đúng": y_openai
})


# Đánh giá thống kê độ đo thống kê (bao nhiêu đỉnh, cạnh, node trung tâm, group).







# vẽ biểu đồ ROC [0-1], accuracy (Y), calculate area 


