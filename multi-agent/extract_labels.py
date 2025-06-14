# from neo4jconnector import Neo4jConnection
# import os
# from dotenv import load_dotenv

# def extract_labels_to_file(output_file: str = "labels/neo4j_labels.txt"):
#     """
#     Extract all labels from Neo4j database and save to file
    
#     Args:
#         output_file: Path to output file
#     """
#     # Load environment variables
#     load_dotenv()
    
#     # Create labels directory if not exists
#     os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
#     # Connect to Neo4j
#     uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
#     user = os.getenv("NEO4J_USER", "neo4j")
#     password = os.getenv("NEO4J_PASSWORD", "password")
#     # database = os.getenv("NEO4J_DATABASE", "neo4j")
#     database = "openai"
    
#     # Initialize connection
#     neo4j_connection = Neo4jConnection(uri, user, password, database)
    
#     try:
#         # Get all labels using Cypher query
#         query = "CALL db.labels()"
#         results = neo4j_connection.run_cypher(query)
        
#         # Extract labels from results
#         labels = sorted([result["label"] for result in results])
        
#         # Write labels to file
#         with open(output_file, "w", encoding="utf-8") as f:
#             for label in labels:
#                 f.write(f"{label}\n")
        
#         print(f"Successfully extracted {len(labels)} name to {output_file}")
        
#     finally:
#         # Close connection
#         neo4j_connection.close()

# if __name__ == "__main__":
#     extract_labels_to_file('labels/neo4j_labels_openai.txt')
    
    
    
    
    #!/usr/bin/env python3
"""
Extract Labels from Neo4j Databases
===================================

Script để trích xuất tất cả labels từ các Neo4j databases
và lưu vào files txt tương ứng.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path to import neo4jconnector
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def extract_labels_from_database(database_name: str, output_file: str) -> bool:
    """
    Trích xuất labels từ một Neo4j database
    
    Args:
        database_name: Tên database Neo4j
        output_file: File output để lưu labels
        
    Returns:
        bool: True nếu thành công, False nếu có lỗi
    """
    try:
        from neo4jconnector import Neo4jConnection
        
        # Load environment variables
        load_dotenv()
        
        # Create labels directory if not exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Connect to Neo4j
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j") 
        password = os.getenv("NEO4J_PASSWORD", "password")
        
        # Initialize connection
        neo4j_connection = Neo4jConnection(uri, user, password, database_name)
        
        # Get all labels using Cypher query
        query = "CALL db.labels()"
        results = neo4j_connection.run_cypher(query)
        
        # Extract labels from results
        labels = sorted([result["label"] for result in results])
        
        # Write labels to file
        with open(output_file, "w", encoding="utf-8") as f:
            for label in labels:
                f.write(f"{label}\n")
        
        print(f"✅ Successfully extracted {len(labels)} labels from {database_name}")
        print(f"   Output: {output_file}")
        print(f"   Labels: {', '.join(labels[:5])}{'...' if len(labels) > 5 else ''}")
        
        # Close connection
        neo4j_connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error extracting labels from {database_name}: {e}")
        return False

def extract_all_labels() -> bool:
    """
    Trích xuất labels từ tất cả databases
    
    Returns:
        bool: True nếu tất cả thành công
    """
    print("🏷️ Trích xuất labels từ Neo4j databases...")
    
    databases_and_files = [
        ("deepseek", "labels/neo4j_labels_deepseek.txt"),
        ("gemini", "labels/neo4j_labels_gemini.txt"), 
        ("openai", "labels/neo4j_labels_openai.txt")
    ]
    
    all_successful = True
    
    for db_name, output_file in databases_and_files:
        print(f"\n📊 Database: {db_name}")
        success = extract_labels_from_database(db_name, output_file)
        if not success:
            all_successful = False
    
    print(f"\n{'='*50}")
    if all_successful:
        print("🎉 Tất cả labels đã được trích xuất thành công!")
        print("\n📁 Files được tạo:")
        for _, output_file in databases_and_files:
            if Path(output_file).exists():
                print(f"   ✅ {output_file}")
            else:
                print(f"   ❌ {output_file}")
    else:
        print("❌ Có lỗi khi trích xuất một số labels")
        print("🔧 Kiểm tra:")
        print("   - Neo4j server đang chạy")
        print("   - Databases deepseek, gemini, openai tồn tại")
        print("   - Cấu hình .env đúng")
        print("   - Kết nối mạng")
    
    return all_successful

def check_labels_files() -> None:
    """Kiểm tra các file labels hiện có"""
    print("📄 Kiểm tra labels files hiện có...")
    
    label_files = [
        "labels/neo4j_labels_deepseek.txt",
        "labels/neo4j_labels_gemini.txt",
        "labels/neo4j_labels_openai.txt"
    ]
    
    print("\nTrạng thái labels files:")
    print("-" * 40)
    
    for file_path in label_files:
        path = Path(file_path)
        if path.exists():
            # Đọc và hiển thị số lượng labels
            with open(path, 'r', encoding='utf-8') as f:
                labels = [line.strip() for line in f if line.strip()]
            print(f"✅ {file_path} ({len(labels)} labels)")
            if labels:
                print(f"   Preview: {', '.join(labels[:3])}{'...' if len(labels) > 3 else ''}")
        else:
            print(f"❌ {file_path} (missing)")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Extract labels from Neo4j databases",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  python extract_labels.py                    # Trích xuất từ tất cả databases
  python extract_labels.py --check           # Chỉ kiểm tra files hiện có
  python extract_labels.py --db deepseek     # Chỉ trích xuất từ deepseek
        """
    )
    
    parser.add_argument('--check', action='store_true', help='Chỉ kiểm tra labels files hiện có')
    parser.add_argument('--db', help='Chỉ trích xuất từ database cụ thể (deepseek/gemini/openai)')
    
    args = parser.parse_args()
    
    print("🏷️ Extract Labels Tool")
    print("=" * 30)
    
    if args.check:
        check_labels_files()
    elif args.db:
        if args.db in ['deepseek', 'gemini', 'openai']:
            output_file = f"labels/neo4j_labels_{args.db}.txt"
            extract_labels_from_database(args.db, output_file)
        else:
            print(f"❌ Database không hợp lệ: {args.db}")
            print("Chọn một trong: deepseek, gemini, openai")
    else:
        extract_all_labels()

if __name__ == "__main__":
    main()
