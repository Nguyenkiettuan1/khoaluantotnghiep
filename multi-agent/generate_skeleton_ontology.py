import os
from dotenv import load_dotenv
from openai import OpenAI
from utils import clean_cypher_code

def generate_ontology_from_cqs(
    qc_folder="Qc",
    output_path="./ontology/ontology_generated.ttl",
    model="gpt-4o-mini"
):
    # Load API key từ file .env
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Bước 1: Đọc toàn bộ các file trong thư mục Qc/
    cq_texts = []
    for filename in sorted(os.listdir(qc_folder)):
        file_path = os.path.join(qc_folder, filename)
        if filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    cq_texts.append(content)
    
    # Bước 2: Gộp danh sách câu hỏi thành văn bản
    cq_combined = "\n".join([f"{i+1}. {q}" for i, q in enumerate(cq_texts)])
    
    # Prompt hệ thống
    system_prompt = (
        "Bạn là chuyên gia ontology. Nhiệm vụ của bạn là trích xuất đầy đủ các thành phần ontology từ danh sách các câu hỏi năng lực về Trường Đại học Sài Gòn.\n\n"
        "Yêu cầu:\n"
        "1. Xác định các lớp (Classes) chính đại diện cho các thực thể được đề cập trong các câu hỏi.\n"
        "2. Xác định các thuộc tính (Properties) kèm theo domain và range phù hợp.\n"
        "3. Xác định các mối quan hệ (Relationship) giữa các lớp dựa trên ngữ cảnh của câu hỏi.\n"
        "4. Chỉ sử dụng các thuật ngữ xuất hiện trong danh sách câu hỏi năng lực.\n"
        "5. Đầu ra phải là mã Turtle thuần túy, khai báo các prefix chuẩn.\n"
        "Trả ra kết quả là mã Turtle chuẩn, hoàn chỉnh, đúng cú pháp.\n"
    )

    # Prompt người dùng
    user_prompt = f"""
    Dưới đây là danh sách các câu hỏi năng lực liên quan đến Trường Đại học Sài Gòn:

    {cq_combined}

    Hãy trích xuất đầy đủ các thành phần để xây dựng một ontology, bao gồm:
    1. Các lớp (Classes) – đại diện cho các thực thể được đề cập trong các câu hỏi.
    2. Các thuộc tính (Properties) – kèm theo domain và range phù hợp.
    3. Các mối quan hệ giữa các lớp – thể hiện cách các lớp liên kết với nhau.

    Trả ra kết quả là mã Turtle thuần túy, không có lời giải thích hay chú thích.
    """

    # Bước 3: Gửi yêu cầu đến LLM
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5
    )
    
    # Bước 4: Lấy kết quả và lưu vào file
    ontology_output = response.choices[0].message.content.strip()
    clean_cypher_code(ontology_output)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ontology_output)
    
    print("✅ Đã tạo ontology và lưu vào:", output_path)
    
if __name__ == "__main__":
    generate_ontology_from_cqs(
        qc_folder="CQs",
        output_path="./ontology/skeleton_ontology.ttl",
        model="gpt-4o-mini"
    )