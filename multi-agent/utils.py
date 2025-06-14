import os
import re
from openai import OpenAI
from dotenv import load_dotenv

import json
from datetime import datetime

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
        temperature=0.3
    )
    
    # Bước 4: Lấy kết quả và lưu vào file
    ontology_output = response.choices[0].message.content.strip()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ontology_output)
    
    print("✅ Đã tạo ontology và lưu vào:", output_path)
def clean_cypher_code(cypher_code: str, remove_trailing_dot: bool = True) -> str:
    """
    Làm sạch mã Cypher:
    - Loại bỏ markdown code block nếu có.
    - Loại bỏ dòng trống và khoảng trắng thừa.
    - Nếu remove_trailing_dot=True, loại bỏ dấu chấm thừa ở cuối mỗi dòng (trừ dòng comment).
    
    Tham số:
    - cypher_code: chuỗi mã Cypher cần làm sạch.
    - remove_trailing_dot: nếu True, xóa dấu chấm cuối dòng (mặc định là True).
    
    Trả về chuỗi mã Cypher đã được làm sạch.
    """
    # Loại bỏ markdown nếu có
    cypher_code = cypher_code.strip()
    if cypher_code.startswith("```turtle") :
        cypher_code = cypher_code.strip("```turtle").strip()
    if cypher_code.endswith("```"):
        cypher_code = cypher_code.strip("```").strip()
    # Tách các dòng và loại bỏ dòng trống
    lines = [line.strip() for line in cypher_code.splitlines() if line.strip()]
    
    cleaned_lines = []
    for line in lines:
        # Nếu dòng không phải là comment và remove_trailing_dot là True,
        # loại bỏ dấu chấm thừa ở cuối dòng
        if remove_trailing_dot and not line.startswith("//"):
            line = re.sub(r'\.\s*$', '', line)
        cleaned_lines.append(line)
    
    # Ghép lại các dòng đã xử lý thành một chuỗi
    final_code = "\n".join(cleaned_lines)
    return final_code.strip()
def validate_cypher_query(query: str, model: str = "gpt-4o-mini") -> dict:
    """Kiểm tra tính hợp lệ của câu truy vấn Cypher"""
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt_path = os.path.join("validate_promt", "cypher_test_prompts.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        test_prompt = f.read()
    
    user_prompt = f"""
    <QUERY>
    {query}
    </QUERY>
    """
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": test_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )
    
    try:
        validation_result = response.choices[0].message.content.strip()
        return validation_result
    except Exception as e:
        return {
            "query": query,
            "is_valid": False,
            "errors": [{
                "location": "LLM processing",
                "reason": str(e),
                "suggestion": "Thử lại với câu truy vấn khác hoặc kiểm tra kết nối"
            }],
            "fixed_query": None
        }

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    generate_ontology_from_cqs()
    # # Example usage
    # run_test_queries_and_save_results(
    #     uri=os.getenv("NEO4J_URI"),
    #     user=os.getenv("NEO4J_USER"),
    #     password=os.getenv("NEO4J_PASSWORD"),
    #     dbname=os.getenv("NEO4J_DATABASE", "neo4j")
    # )
    
