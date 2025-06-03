from rdflib import Graph
import pandas as pd
import os

def extract_relations_to_csv(file_paths: list):
    """
    Trích xuất các quan hệ từ danh sách file ontology TTL và lưu ra file CSV cùng tên.

    Args:
        file_paths (list): Danh sách đường dẫn đến các file TTL (ví dụ: ["deepseek.ttl", "openai.ttl"])
    """
    for path in file_paths:
        try:
            g = Graph()
            g.parse(path, format="ttl")

            relations = []
            for s, p, o in g:
                if isinstance(o, str) and (o.startswith("http") or "#" in o):
                    relations.append({
                        "subject": str(s),
                        "predicate": str(p),
                        "object": str(o)
                    })

            df = pd.DataFrame(relations)
            
            # Lấy tên file không có phần mở rộng để đặt tên file CSV
            base_name = os.path.splitext(os.path.basename(path))[0]
            output_csv = f"{base_name}.csv"

            df.to_csv(f"./ontology/ontology_relations_{output_csv}", index=False, encoding="utf-8-sig")
            print(f"✔ Đã xuất {output_csv} với {len(df)} dòng.")
        except Exception as e:
            print(f"❌ Lỗi xử lý file {path}: {e}")
            
extract_relations_to_csv(["./ontology/deepseek.ttl", "./ontology/gemini.ttl", "./ontology/openai.ttl"])
