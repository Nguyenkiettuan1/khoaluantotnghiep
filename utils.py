import os
from openai import OpenAI
from dotenv import load_dotenv
from neo4jconnector import Neo4jConnection
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

def run_test_queries_and_save_results(
    uri: str, 
    user: str, 
    password: str, 
    dbname: str,
    test_queries_path: str = "testcase/test_queries_cypher.txt",
    output_path: str = "testcase/test_answer_cypher.txt"
):
    """
    Thực thi các câu truy vấn test và lưu kết quả
    
    Args:
        uri: URI kết nối Neo4j
        user: Tên người dùng Neo4j
        password: Mật khẩu Neo4j
        dbname: Tên database
        test_queries_path: Đường dẫn file chứa các câu query test
        output_path: Đường dẫn file để lưu kết quả
    """
    try:
        # Kết nối đến Neo4j
        conn = Neo4jConnection(uri, user, password, dbname)
        print("✅ Đã kết nối thành công đến Neo4j")

        # Đọc file queries
        with open(test_queries_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Tách các câu query riêng biệt
        queries = []
        current_query = []
        current_comment = []
        
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("//"):
                if current_query:  # Nếu đã có query trước đó
                    queries.append({
                        "comment": "\n".join(current_comment),
                        "query": "\n".join(current_query)
                    })
                    current_query = []
                current_comment = [line.lstrip("/ ")]
            elif line:  # Nếu không phải comment và không phải dòng trống
                current_query.append(line)
        
        # Thêm query cuối cùng nếu có
        if current_query:
            queries.append({
                "comment": "\n".join(current_comment),
                "query": "\n".join(current_query)
            })

        # Tạo thư mục output nếu chưa tồn tại
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Thực thi từng query và lưu kết quả
        results = []
        for i, q in enumerate(queries, 1):
            try:
                print(f"Đang thực thi query {i}/{len(queries)}")
                result = conn.run_cypher(q["query"])
                
                results.append({
                    "query_number": i,
                    "description": q["comment"],
                    "query": q["query"],
                    "result": result,
                    "status": "success",
                    "error": None
                })
            except Exception as e:
                results.append({
                    "query_number": i,
                    "description": q["comment"],
                    "query": q["query"],
                    "result": None,
                    "status": "error",
                    "error": str(e)
                })
                print(f"❌ Lỗi khi thực thi query {i}: {str(e)}")

        # Format kết quả và lưu vào file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for r in results:
                f.write(f"## Query {r['query_number']}\n")
                f.write(f"### Description\n{r['description']}\n\n")
                f.write(f"### Query\n```cypher\n{r['query']}\n```\n\n")
                f.write(f"### Status: {r['status']}\n\n")
                
                if r['status'] == 'success':
                    f.write("### Result\n```json\n")
                    f.write(json.dumps(r['result'], indent=2, ensure_ascii=False))
                    f.write("\n```\n\n")
                else:
                    f.write(f"### Error\n```\n{r['error']}\n```\n\n")
                
                f.write("---\n\n")

        print(f"✅ Đã lưu kết quả vào file: {output_path}")
        
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("✅ Đã đóng kết nối Neo4j")

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
    
