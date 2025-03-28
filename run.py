import os
from openai import OpenAI
from dotenv import load_dotenv
from neo4jconnector import Neo4jConnection
from clearCypher import clean_cypher_code
from utils import validate_cypher_query

load_dotenv()

def generate_cypher_from_data_conversation(conversation_messages, client: OpenAI):
    response = client.chat.completions.create(
        messages=conversation_messages,
        model="gpt-4o-mini",
        temperature=0.1,
    )
    cypher_script = response.choices[0].message.content
    for keyword in ["```cypher", "```"]:
        cypher_script = cypher_script.replace(keyword, "")
    return cypher_script.strip()


def generate_cypher_from_data_conversation_DeepSeek(conversation_messages, client: OpenAI = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)):
    response = client.chat.completions.create(
        messages=conversation_messages,
        model="deepseek/deepseek-chat-v3-0324:free",
        temperature=0.1,
    )
    cypher_script = response.choices[0].message.content
    for keyword in ["```cypher", "```"]:
        cypher_script = cypher_script.replace(keyword, "")
    return cypher_script.strip()

# Đường dẫn thư mục chứa các file .txt
dataset_dir = "./dataset"

# File ontology (Turtle)
ontology_file = "./ontology/ontology_generated.ttl"

# Đọc ontology
print("Bắt đầu đọc ontology từ:", ontology_file)
with open(ontology_file, "r", encoding="utf-8") as f:
    ontology = f.read()
print("Đã đọc ontology, độ dài:", len(ontology), "ký tự")

# Thiết lập client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Đảm bảo thư mục cypher tồn tại
os.makedirs("./cypher", exist_ok=True)

# Prompt hệ thống (tiếng Việt)
conversation_messages = [
    {
        "role": "system",
        "content": (
            "Bạn là chuyên gia Neo4j. Dựa trên ontology đã được cung cấp, hãy sinh ra các câu lệnh Cypher MERGE hoặc lệnh tối ưu để đưa dữ liệu vào Neo4j mà không gặp bất cứ lỗi nào khi chạy. "
                "Đảm bảo rằng mã Cypher sinh ra không gây ra lỗi 'Variable already declared' hoặc 'Variable not defined' hay các lỗi cú pháp khác trên Neo4j.\n\n"
                
                "Yêu cầu về đảm bảo tính đầy đủ và chất lượng của knowledge graph:\n"
                "- Mỗi node bắt buộc chỉ có 2 trường name và description.\n"
                "- Đặc biệt: Mỗi node phải có ít nhất một mối quan hệ gián tiếp hoặc trực tiếp với node trung tâm.\n"
                "- Kiểm tra và tạo mối quan hệ hai chiều khi cần thiết (ví dụ: hasTrainingProgram <-> belongsToUniversity).\n"
                "- Mỗi node phải có đầy đủ các thuộc tính bắt buộc từ ontology.\n"
                "- Mỗi node phải có mô tả (description) đầy đủ và chi tiết, càng nhiều thông tin liên quan càng tốt.\n"
                "- Sử dụng OPTIONAL MATCH để kiểm tra và thiết lập các mối quan hệ tiềm năng.\n\n"
                
                "Yêu cầu về cú pháp và tối ưu hóa:\n"
                "- Mỗi node bắt buộc phải có thuộc tính 'name' không cho phép trống và mang tính duy nhất trong cùng một loại node.\n"
                "- Mỗi node bắt buộc phải có thuộc tính 'description' không cho phép trống .\n"
                "- Áp dụng các pattern để match nhiều node và quan hệ trong một câu lệnh, và đảm bảo không khai báo lại biến đã tồn tại.\n\n"
                
                "Yêu cầu về định dạng và kiểu dữ liệu:\n"
                "- Chỉ sử dụng các lớp và thuộc tính được định nghĩa trong ontology.\n"
                "- Không sử dụng dấu hai chấm (:) cho thuộc tính; thay vào đó dùng dấu chấm (.).\n"
                "- Loại bỏ dấu chấm thừa ở cuối câu lệnh.\n"
                "- Chỉ xuất mã Cypher thuần túy, không kèm lời giải thích, chú thích hay markdown.\n\n"
                
                "Hãy duy trì nhất quán các node và quan hệ đã tạo trong toàn bộ cuộc trò chuyện. "
                "Đảm bảo xử lý cả trường hợp node không có dữ liệu hoặc quan hệ bị thiếu, "
                "Mỗi khi tạo một node mới, hãy kiểm tra xem node đó đã tồn tại chưa, "
                "Nếu node đó có cùng ý nghĩa với node đã tồn tại, hãy tái sử dụng node đó."
                "Phải lấy đủ dữ liệu các node và mối quan hệ đã có trong ontology, "
                "và sinh ra các câu lệnh Cypher có thể chạy trên Neo4j mà không gặp bất cứ lỗi nào."
                "Tên các node và mối quan hệ phải sử dụng tiếng Việt không có dấu. Và được phân cách bằng dấu gạch dưới (_)."
        )
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

    # Đọc nội dung file
    with open(file_path, "r", encoding="utf-8") as f:
        data_text = f.read()

    # Truyền toàn bộ nội dung
    user_message = f"""Dữ liệu file: {filename}
    {data_text}

    Ontology:
    {ontology}
    """
    conversation_messages.append({"role": "user", "content": user_message})


    # # Gọi hàm sinh Cypher from open AI
    # generated_cypher = generate_cypher_from_data_conversation(conversation_messages, client)
    
    # # Gọi hàm sinh Cypher from DeepSeek
    generated_cypher = generate_cypher_from_data_conversation_DeepSeek(conversation_messages)
    # Lưu câu trả lời vào conversation để giữ ngữ cảnh
    conversation_messages.append({
        "role": "assistant",
        "content": generated_cypher
    })

    # Lưu vào file riêng
    cypher_file = f"./cypher/{filename}.cypher"
    processed_files.append(cypher_file)
    with open(cypher_file, "w", encoding="utf-8") as f:
        f.write(generated_cypher)
    print(f"✅ Đã lưu Cypher vào file: {cypher_file}")



print(f"\nTất cả các câu lệnh Cypher đã được lưu vào: {processed_files}")

# ================================
# BƯỚC 2: Đẩy dữ liệu lên Neo4j (tuỳ chọn)
# ================================
print("\nBắt đầu kết nối đến Neo4j...")
uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")
dbname = os.getenv("NEO4J_DATABASE")

try:
    conn = Neo4jConnection(uri, neo4j_user, neo4j_password, dbname)
    print("✅ Kết nối đến Neo4j thành công.")

    for cypher_file in processed_files:
        print(f"\n[+] Đang thực thi file: {cypher_file}")
        with open(cypher_file, "r", encoding="utf-8") as f:
            cypher_script = f.read().strip()
        
        if cypher_script:
            result = conn.run_cypher(cypher_script)
            print(f"✅ Thực thi thành công file: {cypher_file}")

except Exception as e:
    print(f"❌ Lỗi: {str(e)}")
finally:
    if 'conn' in locals():
        conn.close()
        print("✅ Đã đóng kết nối Neo4j.")