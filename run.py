import os
from openai import OpenAI
from dotenv import load_dotenv
from neo4jconnector import Neo4jConnection
from clearCypher import clean_cypher_code
from utils import validate_cypher_query

load_dotenv()


# Hàm tạo Cypher từ dữ liệu và ontology sử dụng conversation memory
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
# Đường dẫn thư mục chứa các file .txt
dataset_dir = "./dataset"

# File ontology (Turtle)
ontology_file = "./ontology/ontology_generated.ttl"

# File lưu câu lệnh Cypher
cypher_output_path = "./cypher/populate_ontology.cypher"

# Đọc ontology
print("Bắt đầu đọc ontology từ:", ontology_file)
with open(ontology_file, "r", encoding="utf-8") as f:
    ontology = f.read()
print("Đã đọc ontology, độ dài:", len(ontology), "ký tự")

# Thiết lập client OpenAI
client = OpenAI(api_key=os.getenv("MY_OPENAI_KEY"))

# Xóa file Cypher cũ nếu có
if os.path.exists(cypher_output_path):
    os.remove(cypher_output_path)
    print("Đã xóa file Cypher cũ:", cypher_output_path)

# Prompt hệ thống (tiếng Việt)
conversation_messages = [
    {
        "role": "system",
        "content": (
            "Bạn là chuyên gia Neo4j. Dựa trên ontology được cung cấp, hãy sinh ra các câu lệnh Cypher MERGE tối ưu để đưa dữ liệu vào Neo4j. "
            "Yêu cầu về đảm bảo tính đầy đủ và chất lượng của knowledge graph:\n"
            "1. Đảm bảo mỗi node đều có ít nhất một mối quan hệ với node khác.\n"
            "2. Kiểm tra và tạo mối quan hệ hai chiều khi cần thiết (ví dụ: hasTrainingProgram <-> belongsToUniversity).\n"
            "3. Mỗi node phải có đầy đủ các thuộc tính bắt buộc từ ontology.\n"
            "4. Sử dụng OPTIONAL MATCH để kiểm tra và thiết lập các mối quan hệ tiềm năng.\n"
            "\nYêu cầu về cú pháp và tối ưu hóa:\n"
            "5. Mỗi node phải có thuộc tính 'name' không trống và là duy nhất trong cùng một loại node.\n"
            "6. Nếu một node với cùng 'name' đã được khai báo, tái sử dụng biến đó thay vì khai báo lại.\n"
            "7. Sử dụng WITH để chuỗi các thao tác phức tạp và đảm bảo tính rõ ràng.\n"
            "8. Sử dụng các pattern để match nhiều node và quan hệ trong một câu lệnh.\n"
            "\nYêu cầu về định dạng và kiểu dữ liệu:\n"
            "9. Chỉ sử dụng các lớp và thuộc tính được định nghĩa trong ontology.\n"
            "10. Không sử dụng dấu hai chấm (:) cho thuộc tính, thay vào đó dùng dấu chấm (.).\n"
            "11. Loại bỏ dấu chấm thừa ở cuối câu lệnh.\n"
            "12. Chỉ xuất mã Cypher thuần túy, không kèm giải thích hay markdown.\n"
            "\nHãy duy trì nhất quán các node và quan hệ đã tạo trong toàn bộ cuộc trò chuyện."
            "\nĐảm bảo xử lý cả trường hợp node không có dữ liệu hoặc quan hệ bị thiếu."
        )
    },
]

# Lấy danh sách file .txt trong thư mục dataset
txt_files = [f for f in os.listdir(dataset_dir) if f.endswith(".txt")]

# Lọc chỉ những file có tên chứa "PHẦN 1"
txt_files_phan1 = [f for f in txt_files if "PHẦN 1" in f]

# Có thể sắp xếp để đọc theo thứ tự
txt_files_phan1.sort()

all_generated_cypher = ""

for idx, filename in enumerate(txt_files_phan1, start=1):
    file_path = os.path.join(dataset_dir, filename)
    print(f"\n[+] Đang xử lý file {idx}: {filename}")

    # Đọc nội dung file
    with open(file_path, "r", encoding="utf-8") as f:
        data_text = f.read()

    # Ở đây, ví dụ không chia chunk, mà truyền trực tiếp toàn bộ nội dung
    chunk = data_text

    user_message = f"""Dữ liệu file: {filename}
    {chunk}

    Ontology:
    {ontology}

    Hãy sinh các câu lệnh Cypher MERGE để đưa dữ liệu vào Neo4j với các lưu ý sau:
    - Nếu một node đã được khai báo (ví dụ: node University với {{name: 'Trường Đại học Sài Gòn'}}), hãy sử dụng lại biến đó thay vì tái khai báo.
    - Tương tự, nếu các node khác (ví dụ: TrainingProgram, Department, ...) đã được khai báo, hãy tái sử dụng chúng.
    - Không thêm dấu chấm thừa ở cuối các câu lệnh.
    Trả ra kết quả là mã Cypher thuần túy, không có lời giải thích, chú thích hay markdown.
    """
    conversation_messages.append({"role": "user", "content": user_message})

    # Gọi hàm sinh Cypher
    generated_cypher = generate_cypher_from_data_conversation(conversation_messages, client)

    # Lưu câu trả lời vào conversation để giữ ngữ cảnh
    conversation_messages.append({
        "role": "assistant",
        "content": generated_cypher
    })

    # # Làm sạch câu lệnh Cypher (nếu có hàm clean_cypher_code)
    # generated_cypher = clean_cypher_code(generated_cypher, remove_trailing_dot=True)

    # # Kiểm tra Cypher (nếu có hàm validate_cypher_query)
    # check_cypher = validate_cypher_query(generated_cypher)

    # Lưu vào biến tổng
    all_generated_cypher += f"// Từ file {filename}\n" + generated_cypher + "\n\n"

    # Ghi ngay vào file cypher
    with open(cypher_output_path, "a", encoding="utf-8") as f:
        f.write(generated_cypher + "\n")

print(f"\nTất cả các câu lệnh Cypher đã được lưu vào: {cypher_output_path}")

# Làm sạch toàn bộ nội dung Cypher (loại bỏ markdown nếu có)
with open(cypher_output_path, "r", encoding="utf-8") as f:
    cypher_script = f.read().strip()

for keyword in ["```cypher", "```"]:
    cypher_script = cypher_script.replace(keyword, "")

cypher_script = cypher_script.strip()
with open(cypher_output_path, "w", encoding="utf-8") as f:
    f.write(cypher_script)
print(f"✅ Mã Cypher đã được làm sạch và lưu vào: {cypher_output_path}")

# ================================
# BƯỚC 2: Đẩy dữ liệu lên Neo4j (tuỳ chọn)
# ================================
print("\nBắt đầu kết nối đến Neo4j...")
uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")
dbname = os.getenv("NEO4J_DATABASE")

conn = Neo4jConnection(uri, neo4j_user, neo4j_password, dbname)
print("✅ Kết nối đến Neo4j thành công.")

result = conn.run_cypher(cypher_script)
print("✅ Dữ liệu đã được đưa vào Neo4j!")
conn.close()
print("✅ Đã đóng kết nối Neo4j.")