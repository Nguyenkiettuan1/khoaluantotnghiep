import os
from google.generativeai import GenerativeModel
from dotenv import load_dotenv
from neo4jconnector import Neo4jConnection
from clearCypher import clean_cypher_code
from gemini_config import gemini

load_dotenv()

def generate_cypher_from_data_conversation(conversation_messages):
    # Format conversation for Gemini
    formatted_messages = "\n".join([
        f"{msg['role']}: {msg['parts']}" 
        for msg in conversation_messages
    ])
    
    # Get response using GeminiConfig instance
    response = gemini.generate_response(formatted_messages)
    
    # Clean up cypher script
    cypher_script = clean_cypher_code(response)
    
    # Validate cypher script
    
        
    return cypher_script

# Đường dẫn thư mục chứa các file .txt
dataset_dir = "./dataset"

# File ontology (Turtle)
ontology_file = "./ontology/ontology_generated.ttl"

try:
    # Đọc ontology
    print("Bắt đầu đọc ontology từ:", ontology_file)
    with open(ontology_file, "r", encoding="utf-8") as f:
        ontology = f.read()
    print("Đã đọc ontology, độ dài:", len(ontology), "ký tự")

    # Đảm bảo thư mục cypher tồn tại
    os.makedirs("./cypher_gemini", exist_ok=True)

    # Prompt hệ thống (tiếng Việt)
    conversation_messages = [
        {
            "role": "user",
            "parts": [
                "Bạn là chuyên gia Neo4j. Dựa trên ontology đã được cung cấp, hãy sinh ra các câu lệnh Cypher MERGE để đưa dữ liệu vào Neo4j mà không gặp bất cứ lỗi về cú pháp nào khi chạy. "
                "Yêu cầu về đảm bảo tính đầy đủ và chất lượng của knowledge graph:\n"
                "- Mỗi node bắt buộc chỉ có 2 trường name và description.\n"
                "- Mỗi node phải có ít nhất một mối quan hệ gián tiếp hoặc trực tiếp với node trung tâm.\n"
                "- Kiểm tra và tạo mối quan hệ hai chiều khi cần thiết (ví dụ: hasTrainingProgram <-> belongsToUniversity).\n"
                "- Mỗi node phải có mô tả (description) đầy đủ và chi tiết, càng nhiều thông tin liên quan càng tốt.\n"
                "- Sử dụng OPTIONAL MATCH để kiểm tra và thiết lập các mối quan hệ tiềm năng.\n\n"
                
                "Yêu cầu về cú pháp và tối ưu hóa:\n"
                "- Mỗi class nên được tạo riêng biệt, và tránh gốp quá nhiều MERGE vào cùng một câu.\n"
                "- Sử dụng WITH hợp lý để truyền biến giữa các bước,đảm bảo không bị lỗi 'WITH is required between MERGE and MATCH', sử dụng đúng cú pháp.\n"
                "- Mỗi node bắt buộc phải có thuộc tính 'name' không cho phép trống và mang tính duy nhất trong cùng một loại node.\n"
                "- Mỗi node bắt buộc phải có thuộc tính 'description' không cho phép trống .\n"
                "- Áp dụng các pattern để match nhiều node và quan hệ trong một câu lệnh, và đảm bảo không khai báo lại biến đã tồn tại.\n\n"
                
                "Yêu cầu về định dạng và kiểu dữ liệu:\n"
                "- Sử dụng các lớp và thuộc tính được định nghĩa trong ontology, có thể mở rộng ra.\n"
                "- Không sử dụng dấu hai chấm (:) cho thuộc tính; thay vào đó dùng dấu chấm (.).\n"
                "- Loại bỏ dấu chấm thừa ở cuối câu lệnh.\n"
                "- Chỉ xuất mã Cypher thuần túy, không kèm lời giải thích, chú thích hay markdown.\n\n"
                
                "Hãy duy trì nhất quán các node và quan hệ đã tạo trong toàn bộ cuộc trò chuyện. "
                "Chỉ tạo các node có ý nghĩa để tạo 1 knowledge graph."
                "Đảm bảo xử lý cả trường hợp node không có dữ liệu hoặc quan hệ bị thiếu, "
                "Mỗi khi tạo một node mới, hãy kiểm tra xem node đó đã tồn tại chưa, "
                "Nếu node đó có cùng ý nghĩa với node đã tồn tại, hãy tái sử dụng node đó."
                "Sinh ra các câu lệnh Cypher có thể chạy trên Neo4j mà không gặp bất cứ lỗi nào."
              
            ]
        },
    ]

    # Lấy danh sách file .txt trong thư mục dataset
    txt_files = [f for f in os.listdir(dataset_dir) if f.endswith(".txt")]

    # Lọc chỉ những file có tên chứa "PHẦN 1"
    txt_files_phan1 = [f for f in txt_files if "PHẦN 1" in f]
    txt_files_phan1.sort()

    # Xử lý từng file và lưu vào file riêng
    processed_files = []
    for idx, filename in enumerate(txt_files_phan1, start=1):
        file_path = os.path.join(dataset_dir, filename)
        print(f"\n[+] Đang xử lý file {idx}: {filename}")

        try:
            # Đọc nội dung file
            with open(file_path, "r", encoding="utf-8") as f:
                data_text = f.read()

            # Truyền toàn bộ nội dung
            user_message = f"""Dữ liệu file: {filename}
            {data_text}

            Ontology:
            {ontology}
            Chỉ tạo cypher dựa trên các node và mối quan hệ đã có trong ontology.
            """
            conversation_messages.append({"role": "user", "parts": [user_message]})

            # Sinh Cypher
            generated_cypher = generate_cypher_from_data_conversation(conversation_messages)
            conversation_messages.append({
                "role": "assistant",
                "parts": [generated_cypher]
            })

            # Lưu vào file riêng
            cypher_file = f"./cypher_gemini/{filename}.cypher"
            processed_files.append(cypher_file)
            with open(cypher_file, "w", encoding="utf-8") as f:
                f.write(generated_cypher)
            print(f"✅ Đã lưu Cypher vào file: {cypher_file}")
            
        except Exception as e:
            print(f"❌ Lỗi khi xử lý file {filename}: {str(e)}")
            continue

   

except Exception as e:
    print(f"❌ Lỗi khởi tạo: {str(e)}")