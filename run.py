import os
from pdf_to_images import convert_pdf_to_images
from image_to_llm import process_images
from utils import generate_cypher_commands, execute_cypher
from dotenv import load_dotenv

load_dotenv()

def main():
    """Main function to coordinate the entire process"""
    print("=== BẮT ĐẦU QUÁ TRÌNH XỬ LÝ ===")
    
    # Step 1: Convert PDF to images if needed
    if not os.path.exists("images") or not os.listdir("images"):
        print("\n1. Chuyển đổi PDF thành ảnh...")
        convert_pdf_to_images(
            pdf_path="data/p1.pdf",
            output_dir="images",
            start_page=5,
            end_page=13
        )
    else:
        print("\n1. Đã có thư mục ảnh, bỏ qua bước chuyển đổi PDF")
    
    # Step 2: Process images to create TTL ontology
    print("\n2. Đang tạo ontology từ ảnh...")
    process_images()
    
    # Step 3: Check for ontology file
    if not os.path.exists("ontology/ontology_generated.ttl"):
        print("\n❌ Không tìm thấy file ontology/ontology_generated.ttl")
        print("Có lỗi trong quá trình tạo ontology")
        return
    else:
        print("✅ Đã tạo xong file ontology")
    
    # Step 4: Generate Cypher commands
    print("\n3. Đang tạo câu lệnh Cypher từ ảnh và ontology...")
    cypher_commands = generate_cypher_commands()
    if cypher_commands:
        print(f"✅ Đã tạo {len(cypher_commands)} câu lệnh Cypher")
        print("Đã lưu vào cypher/populate_ontology.cypher")
    else:
        print("❌ Không tạo được câu lệnh Cypher")
        return
    
    # Step 5: Execute Cypher commands
    print("\n4. Đang thực thi câu lệnh Cypher...")
    neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    neo4j_user = os.getenv("NEO4J_USER", "neo4j")
    neo4j_password = os.getenv("NEO4J_PASSWORD")
    
    if neo4j_password:
        execute_cypher(cypher_commands, neo4j_uri, neo4j_user, neo4j_password)
        print("✅ Đã thực thi tất cả câu lệnh Cypher")
    else:
        print("❌ Thiếu thông tin đăng nhập Neo4j")
    
    print("\n=== HOÀN THÀNH ===")

if __name__ == "__main__":
    # Check environment variables
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API key",
        "NEO4J_PASSWORD": "Neo4j password"
    }
    
    missing_vars = []
    for var, desc in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"{var} ({desc})")
    
    if missing_vars:
        print("❌ Thiếu các biến môi trường sau trong file .env:")
        for var in missing_vars:
            print(f"- {var}")
        exit(1)
    
    try:
        main()
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        print("\nVui lòng kiểm tra:")
        print("1. File .env có chứa OPENAI_API_KEY và NEO4J_PASSWORD")
        print("2. File PDF nguồn tồn tại trong thư mục data/")
        print("3. Kết nối Neo4j hoạt động")
        print("4. Đã cài đặt đầy đủ thư viện")
