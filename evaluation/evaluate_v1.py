from rdflib import Graph, Literal
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
import re
import pandas as pd

# Định nghĩa lại hàm evaluate_text_match và compute_metrics vì kernel đã reset
def evaluate_text_match(graph, answers):
    result = []
    for answer in answers:
        found = False
        for s, p, o in graph:
            if isinstance(o, Literal) and any(word.lower() in str(o).lower() for word in answer.lower().split()[:5]):
                found = True
                break
        result.append(found)
    return result

def compute_metrics(y_pred):
    y_true = [True] * len(y_pred)
    return {
        "Accuracy": round(accuracy_score(y_true, y_pred), 3),
        "Precision": round(precision_score(y_true, y_pred, zero_division=0), 3),
        "Recall": round(recall_score(y_true, y_pred, zero_division=0), 3),
        "F1 Score": round(f1_score(y_true, y_pred, zero_division=0), 3)
    }


# Load 3 RDF Graphs from LLMs
g_deepseek = Graph().parse("../ontology/cleaned_deepseek_v3_0324.ttl", format="turtle")
g_gemini = Graph().parse("../ontology/cleaned_gemini_flash_thinking.ttl", format="turtle")
g_openai = Graph().parse("../ontology/cleaned_openai_4o_mini.ttl", format="turtle")

# Câu trả lời chuẩn từ CQ_SGU
with open("../QC/CQ_SGU.txt", "r", encoding="utf-8") as f:
    questions = [line.strip() for line in f.readlines() if line.strip()]

# Trích lọc từ câu trả lời chuẩn trước đó (được tạo từ mã trước)
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
# Hàm trích các keyword chính (có thể thay bằng TF-IDF hoặc spaCy nếu muốn mở rộng)
def extract_keywords(text):
    words = re.findall(r'\w+', text.lower())
    blacklist = {"trường", "đại", "học", "sài", "gòn", "là", "các", "có", "và", "với", "tại", "trên", "của", "được"}
    return [w for w in words if w not in blacklist and len(w) > 2]

def evaluate_text_match_with_output(graph, answers):
    result = []
    for answer in answers:
        keywords = extract_keywords(answer)
        matched_literal = ""
        for s, p, o in graph:
            if isinstance(o, Literal):
                literal_text = str(o).lower()
                match_score = sum(1 for kw in keywords if kw in literal_text)
                if match_score >= max(2, len(keywords) // 3):  # điều kiện đủ tốt
                    matched_literal = str(o)
                    break
        result.append(matched_literal)
    return result

# Hàm so khớp theo số lượng từ khóa tìm thấy trong triple
def evaluate_text_match(graph, answers):
    result = []
    for answer in answers:
        keywords = extract_keywords(answer)
        found = False
        for s, p, o in graph:
            if isinstance(o, Literal):
                literal_text = str(o).lower()
                match_score = sum(1 for kw in keywords if kw in literal_text)
                if match_score >= max(2, len(keywords) // 3):  # ngưỡng đủ tin cậy
                    found = True
                    break
        result.append(found)
    return result

# Evaluate for each model
y_true = [True] * len(answers_split)

# Compile results
def compute_metrics(y_pred):
    return {
        "Accuracy": round(accuracy_score(y_true, y_pred), 3),
        "Precision": round(precision_score(y_true, y_pred, zero_division=0), 3),
        "Recall": round(recall_score(y_true, y_pred, zero_division=0), 3),
        "F1 Score": round(f1_score(y_true, y_pred, zero_division=0), 3)
    }

# Đánh giá lại
y_deepseek = evaluate_text_match(g_deepseek, answers_split)
y_gemini = evaluate_text_match(g_gemini, answers_split)
y_openai = evaluate_text_match(g_openai, answers_split)

# Tính toán chỉ số
evaluation_df = pd.DataFrame({
    "DeepSeek": compute_metrics(y_deepseek),
    "Gemini": compute_metrics(y_gemini),
    "OpenAI": compute_metrics(y_openai)
}).T

print("\n--- Bảng đánh giá ---")
print(evaluation_df)


# Áp dụng cho từng mô hình
matched_deepseek = evaluate_text_match_with_output(g_deepseek, answers_split)
matched_gemini = evaluate_text_match_with_output(g_gemini, answers_split)
matched_openai = evaluate_text_match_with_output(g_openai, answers_split)

# Tạo bảng kết quả chi tiết
df_matches = pd.DataFrame({
    "Câu hỏi": questions,
    "Đáp án chuẩn": answers_split,
    "DeepSeek trả lời": matched_deepseek,
    "Gemini trả lời": matched_gemini,
    "OpenAI trả lời": matched_openai
})



# Lưu kết quả vào file CSV
# Xuất file CSV
df_matches.to_csv("ket_qua_tra_loi_cua_moi_mo_hinh.csv", index=False, encoding="utf-8-sig")
print("✅ Đã lưu file 'ket_qua_tra_loi_cua_moi_mo_hinh.csv'.")



# Tạo bảng hiển thị các câu sai/thiếu của từng mô hình
wrong_df = pd.DataFrame({
    "Câu hỏi": questions,
    "DeepSeek đúng": y_deepseek,
    "Gemini đúng": y_gemini,
    "OpenAI đúng": y_openai
})

# Lọc ra các câu không được tất cả mô hình trả lời đúng
wrong_df_filtered = wrong_df[~(wrong_df["DeepSeek đúng"] & wrong_df["Gemini đúng"] & wrong_df["OpenAI đúng"])]


# Xuất kết quả ra CSV
wrong_df_filtered.to_csv("cau_hoi_sai_or_thieu.csv", index=False, encoding="utf-8-sig")
print("✅ Đã lưu file 'cau_hoi_sai_or_thieu.csv' thành công.")
