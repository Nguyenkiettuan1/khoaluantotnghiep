import os
from openai import OpenAI
from dotenv import load_dotenv
from neo4jconnector import Neo4jConnection
from clearCypher import clean_cypher_code
from utils import validate_cypher_query

load_dotenv()



# Hàm chia nhỏ văn bản theo độ dài tối đa
def split_text(text, max_length=3000):
    sentences = text.split('. ')
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_length:
            current_chunk += sentence + '. '
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + '. '
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

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

# ================================
# ĐƯỜNG DẪN & KHỞI TẠO
# ================================
data_file = "./dataset/full_text.txt"         # File chứa dữ liệu gộp
ontology_file = "./ontology/ontology_generated.ttl"  # File ontology (Turtle)
cypher_output_path = "./cypher/populate_ontology.cypher"  # File lưu các câu lệnh Cypher

print("Bắt đầu đọc dữ liệu từ:", data_file)
with open(data_file, "r", encoding="utf-8") as f:
    data_text = f.read()
print("Đã đọc dữ liệu, độ dài:", len(data_text), "ký tự")

print("Bắt đầu đọc ontology từ:", ontology_file)
with open(ontology_file, "r", encoding="utf-8") as f:
    ontology = f.read()
print("Đã đọc ontology, độ dài:", len(ontology), "ký tự")

# Chia nhỏ dữ liệu thành các đoạn (chunk) nhỏ
data_chunks = split_text(data_text, max_length=3000)
print(f"Đã chia dữ liệu thành {len(data_chunks)} đoạn.")

# Thiết lập client OpenAI
client = OpenAI(api_key=os.getenv("MY_OPENAI_KEY"))

# Xóa file Cypher cũ nếu có
if os.path.exists(cypher_output_path):
    os.remove(cypher_output_path)
    print("Đã xóa file Cypher cũ:", cypher_output_path)

# ================================
# BƯỚC 1: Sinh câu lệnh Cypher MERGE từ dữ liệu qua conversation
# ================================
# Prompt hệ thống (tiếng Việt)
# Chú ý: Yêu cầu LLM chỉ khai báo node University một lần. Nếu node đã được tạo, hãy tái sử dụng biến đó.
conversation_messages = [
    {
        "role": "system",
        "content": (
            "Bạn là chuyên gia Neo4j. Dựa trên ontology được cung cấp, hãy sinh ra các câu lệnh Cypher MERGE tối ưu để đưa dữ liệu vào Neo4j. "
            "Các yêu cầu:\n"
            "1. Mỗi node phải có thuộc tính 'name' không trống.\n"
            "2. Nếu một node với cùng thuộc tính 'name' đã được khai báo (ví dụ: biến 'university'), hãy tái sử dụng biến đó, không khai báo lại.\n"
            "3. Câu lệnh Cypher phải được tối ưu và chạy được trên Neo4j.\n"
            "4. Chỉ xuất ra mã Cypher thuần túy, không có lời giải thích, chú thích hay định dạng markdown.\n"
            "5. Chỉ sử dụng các lớp và thuộc tính đã được định nghĩa trong ontology.\n"
            "6. Không sử dụng dấu hai chấm (:) để truy cập thuộc tính; hãy dùng dấu chấm (.) (ví dụ: SET university.hasType = '...' ).\n"
            "7. Không thêm dấu chấm thừa ở cuối các câu lệnh.\n"
            "8. Mỗi node phải có ít nhất một quan hệ với một node khác.\n"
            "Hãy ghi nhớ toàn bộ các câu lệnh đã sinh ra trong cuộc trò chuyện này để duy trì tính nhất quán."
    )
    },
]

all_generated_cypher = ""
print("Bắt đầu sinh câu lệnh Cypher từ dữ liệu...")

for idx, chunk in enumerate(data_chunks):
    print(f"\nĐang xử lý đoạn {idx+1} ...")
    # Kiểm tra nếu chunk chứa "PHẦN 2"
    if "PHẦN 2" in chunk:
        answer = input(f"Đoạn {idx+1} chứa 'PHẦN 2'. Bạn có muốn tiếp tục xử lý các đoạn sau sau khi xử lý đoạn này không? (y/n): ")
    else:
        answer = "y"
    
    # Thêm dữ liệu đoạn hiện tại vào conversation
    conversation_messages.append({
        "role": "user",
        "content": f"""Dữ liệu đoạn {idx+1}:
    {chunk}

    Ontology:
    {ontology}

    Hãy sinh các câu lệnh Cypher MERGE để đưa dữ liệu vào Neo4j với các lưu ý sau:
    - Nếu một node đã được khai báo (ví dụ: node University với {{name: 'Trường Đại học Sài Gòn'}}), hãy sử dụng lại biến đó thay vì tái khai báo.
    - Tương tự, nếu các node khác (ví dụ: TrainingProgram, Department, ...) đã được khai báo, hãy tái sử dụng chúng.
    - Không thêm dấu chấm thừa ở cuối các câu lệnh.
    Trả ra kết quả là mã Cypher thuần túy, không có lời giải thích, chú thích hay markdown."""
    })


    generated_cypher = generate_cypher_from_data_conversation(conversation_messages, client)
    
    conversation_messages.append({
        "role": "assistant",
        "content": generated_cypher
    })
    # generated_cypher = clean_cypher_code(generated_cypher, remove_trailing_dot=True)
    # check_cypher = validate_cypher_query(generated_cypher)
    all_generated_cypher += f"// Từ đoạn {idx+1}\n" + generated_cypher + "\n\n"
    with open(cypher_output_path, "a", encoding="utf-8") as f:
        f.write(generated_cypher + "\n")
    print(f"✅ Đã sinh câu lệnh Cypher cho đoạn {idx+1}")
    
    if "PHẦN 2" in chunk and answer.lower() != "y":
        print("Dừng xử lý các đoạn tiếp theo theo yêu cầu của người dùng.")
        break

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
# BƯỚC 2: Đẩy dữ liệu lên Neo4j
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
