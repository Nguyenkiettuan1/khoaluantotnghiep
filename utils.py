import os
import base64
from openai import OpenAI
from typing import List, Dict
import json
import re
import time
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

def encode_image(image_path: str) -> str:
    """Encode a single image to base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def load_ontology() -> str:
    """Load existing TTL ontology file"""
    ttl_path = "ontology/ontology_generated.ttl"
    if not os.path.exists(ttl_path):
        raise FileNotFoundError(f"Không tìm thấy file ontology: {ttl_path}")
    
    with open(ttl_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_json_from_response(response_text: str) -> Dict:
    """Extract and parse JSON from model response"""
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        try:
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                return json.loads(json_match.group(0))
            
            entities = []
            relationships = []
            
            entity_pattern = r'(?:Entity|Node):\s*{([^}]*)}'
            relationship_pattern = r'(?:Relationship|Relation):\s*{([^}]*)}'
            
            for match in re.finditer(entity_pattern, response_text, re.IGNORECASE):
                try:
                    entity_text = "{" + match.group(1) + "}"
                    entity = json.loads(entity_text)
                    entities.append(entity)
                except:
                    continue
                    
            for match in re.finditer(relationship_pattern, response_text, re.IGNORECASE):
                try:
                    rel_text = "{" + match.group(1) + "}"
                    relationship = json.loads(rel_text)
                    relationships.append(relationship)
                except:
                    continue
                    
            return {
                "entities": entities,
                "relationships": relationships
            }
            
        except Exception as e:
            print(f"❌ Lỗi khi xử lý phản hồi: {str(e)}")
            print("Phản hồi gốc:")
            print(response_text)
            raise ValueError("Không thể xử lý phản hồi từ model")

def analyze_images_batch(image_paths: List[str], ttl_content: str, previous_cypher: str = None) -> Dict:
    """Analyze a batch of images using GPT-4-vision with reference to existing ontology"""
    client = OpenAI()
    
    content = [
        {
            "type": "text",
            "text": f"""Phân tích nội dung trong các ảnh và trả về dưới dạng JSON với cấu trúc:
            {{
                "entities": [
                    {{
                        "type": "Loại thực thể theo ontology",
                        "name": "Tên thực thể",
                        "properties": {{
                            "key": "value"
                        }}
                    }}
                ],
                "relationships": [
                    {{
                        "from": "Thực thể nguồn",
                        "type": "Loại quan hệ theo ontology",
                        "to": "Thực thể đích",
                        "properties": {{
                            "key": "value"
                        }}
                    }}
                ]
            }}"""
        }
    ]

    if previous_cypher:
        content[0]["text"] += f"\n\nĐảm bảo kết quả phù hợp với các câu lệnh Cypher đã tạo trước đó:\n{previous_cypher}"
    
    # Process images
    total_size = 0
    for image_path in image_paths:
        if not os.path.exists(image_path):
            print(f"⚠️ Bỏ qua file không tồn tại: {image_path}")
            continue
            
        file_size = os.path.getsize(image_path)
        if file_size > 20 * 1024 * 1024:  # 20MB limit
            print(f"⚠️ Bỏ qua file quá lớn: {image_path}")
            continue
            
        total_size += file_size
        if total_size > 100 * 1024 * 1024:  # 100MB total batch limit
            print("⚠️ Đã đạt giới hạn kích thước batch")
            break
            
        base64_image = encode_image(image_path)
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_image}",
                "detail": "low"
            }
        })
    
    if len(content) == 1:  # No valid images added
        return None
        
    messages = [
        {
            "role": "system",
            "content": f"""Bạn là một chuyên gia phân tích nội dung và tạo câu lệnh Cypher.
            Sử dụng ontology sau làm tham chiếu cho cấu trúc dữ liệu:

            {ttl_content}

            Nhiệm vụ của bạn là:
            1. Phân tích nội dung trong tất cả các ảnh
            2. Trích xuất các thực thể và mối quan hệ theo ontology
            3. Trả về kết quả CHÍNH XÁC theo cấu trúc JSON được yêu cầu
            4. KHÔNG được thêm bất kỳ giải thích hay comment nào khác

            Lưu ý:
            - Đảm bảo các loại thực thể và quan hệ phù hợp với ontology
            - Tên thuộc tính phải theo định nghĩa trong ontology
            - Dữ liệu phải có tính liên kết và nhất quán
            - Trích xuất càng nhiều thông tin càng tốt
            - CHỈ trả về JSON, không thêm text hay comment"""
        },
        {
            "role": "user",
            "content": content
        }
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Corrected model name
            messages=messages,
            max_tokens=4096,
            temperature=0
        )
        
        time.sleep(2)  # Wait to avoid rate limiting
        
        response_text = response.choices[0].message.content
        result = extract_json_from_response(response_text)
        
        if not isinstance(result, dict):
            raise ValueError("Kết quả không phải là dictionary")
        if "entities" not in result or "relationships" not in result:
            raise ValueError("Kết quả thiếu entities hoặc relationships")
            
        return result
        
    except Exception as e:
        print(f"❌ Lỗi khi phân tích ảnh: {str(e)}")
        return None

def escape_cypher_string(s: str) -> str:
    """Escape special characters in Cypher strings"""
    return s.replace("'", "\\'")

def validate_relationships(entities: List[Dict], relationships: List[Dict]) -> List[Dict]:
    """Validate relationships against existing entities"""
    entity_names = {entity["name"] for entity in entities}
    valid_relationships = []
    
    for rel in relationships:
        if rel["from"] in entity_names and rel["to"] in entity_names:
            valid_relationships.append(rel)
        else:
            print(f"⚠️ Bỏ qua quan hệ không hợp lệ: {rel['from']} -> {rel['to']}")
            
    return valid_relationships

def generate_cypher_commands(image_dir: str = "images", batch_size: int = 5) -> List[str]:
    """Generate Cypher commands by processing images in batches using LLM"""
    print("Đang tạo câu lệnh Cypher từ các ảnh...")
    
    if not os.path.exists(image_dir):
        print(f"❌ Thư mục ảnh không tồn tại: {image_dir}")
        return []
    
    try:
        ttl_content = load_ontology()
        print("✅ Đã tải ontology")
    except FileNotFoundError as e:
        print(f"❌ {str(e)}")
        return []
    
    images = [f for f in sorted(os.listdir(image_dir)) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        print("❌ Không tìm thấy ảnh trong thư mục")
        return []
    
    # Process in smaller batches for better efficiency
    if batch_size <= 0:
        batch_size = 5  # Default batch size
        
    cypher_commands = []
    previous_cypher = None
    
    for i in range(0, len(images), batch_size):
        batch = images[i:i + batch_size]
        image_paths = [os.path.join(image_dir, image) for image in batch]
        print(f"\nĐang phân tích batch {i//batch_size + 1}/{(len(images) + batch_size - 1)//batch_size}...")
        
        if previous_cypher:
            print("Sử dụng câu lệnh Cypher trước đó để đảm bảo tính nhất quán...")
            
        # Generate Cypher commands using LLM
        result = analyze_images_batch(image_paths, ttl_content, previous_cypher)
        
        if not result:
            continue
            
        # Use LLM to generate Cypher commands for nodes
        entity_content = {
            "role": "system",
            "content": """Generate Neo4j Cypher commands for creating nodes with the following requirements:
            1. Use MERGE to avoid duplicates
            2. Properly escape all property values
            3. Use parameterized queries where possible
            4. Validate node labels
            Return only the Cypher commands without any explanation."""
        }
        
        try:
            client = OpenAI()
            for entity in result.get("entities", []):
                entity["properties"]["name"] = escape_cypher_string(entity["name"])
                entity_response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        entity_content,
                        {"role": "user", "content": f"Create a node of type {entity['type']} with properties: {entity['properties']}"}
                    ],
                    temperature=0
                )
                command = entity_response.choices[0].message.content.strip()
                if command:
                    cypher_commands.append(command)
            
            # Use LLM to generate Cypher commands for relationships
            valid_relationships = validate_relationships(
                result.get("entities", []),
                result.get("relationships", [])
            )
            
            rel_content = {
                "role": "system",
                "content": """Generate Neo4j Cypher commands for creating relationships with the following requirements:
                1. Use MERGE to avoid duplicates
                2. Properly escape all property values
                3. Match nodes using unique identifiers
                4. Validate relationship types
                Return only the Cypher commands without any explanation."""
            }
            
            for rel in valid_relationships:
                rel_response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        rel_content,
                        {"role": "user", "content": f"Create a relationship of type {rel['type']} from node '{escape_cypher_string(rel['from'])}' to '{escape_cypher_string(rel['to'])}' with properties: {rel.get('properties', {})}"}
                    ],
                    temperature=0
                )
                command = rel_response.choices[0].message.content.strip()
                if command:
                    cypher_commands.append(command)
                    
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"❌ Lỗi khi tạo câu lệnh Cypher: {str(e)}")
            continue
            
        # Save progress
        if cypher_commands:
            current_commands = ';\n'.join(cypher_commands)
            previous_cypher = current_commands
            
            os.makedirs('cypher', exist_ok=True)
            with open('cypher/populate_ontology.cypher', 'w', encoding='utf-8') as f:
                f.write(current_commands + ';')
    
    if cypher_commands:
        print(f"✅ Đã tạo {len(cypher_commands)} câu lệnh Cypher")
    else:
        print("❌ Không tạo được câu lệnh Cypher nào")
    
    return cypher_commands

def execute_cypher(cypher_commands: List[str], neo4j_uri: str, username: str, password: str):
    """Execute Cypher commands in Neo4j"""
    if not cypher_commands:
        print("Không có câu lệnh Cypher nào để thực thi")
        return
        
    driver = GraphDatabase.driver(neo4j_uri, auth=(username, password))
    
    try:
        with driver.session() as session:
            for command in cypher_commands:
                command = command.strip()
                if command:  # Skip empty commands
                    print(f"Executing: {command[:100]}...")  # Show first 100 chars
                    session.run(command)
                    time.sleep(0.1)  # Small delay between commands
                    
    except Exception as e:
        print(f"❌ Lỗi khi thực thi Cypher: {str(e)}")
        raise e
        
    finally:
        driver.close()
