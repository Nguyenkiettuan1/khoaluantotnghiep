import os
import pandas as pd
from collections import defaultdict

# Bản đồ tên file ontology của từng client
path_map = {
    "deepseek": "./ontology/ontology_relations_deepseek.csv",
    "gemini":   "./ontology/ontology_relations_gemini.csv",
    "openai":   "./ontology/ontology_relations_openai.csv"
}

# Thư mục để lưu kết quả precompute
output_dir = "./precomputed_relations"
os.makedirs(output_dir, exist_ok=True)

for client_name, csv_path in path_map.items():
    if not os.path.exists(csv_path):
        print(f"Không tìm thấy {csv_path}, bỏ qua {client_name}")
        continue

    df = pd.read_csv(csv_path)
    # Tạo map: entity_name -> list of (predicate, other_entity)
    # (cả khi entity đứng ở vị trí subject hoặc object)
    direct_map = defaultdict(list)

    for rel in df.to_dict(orient="records"):
        subj = rel["subject"].split("#")[-1].replace("_", " ").strip()
        obj  = rel["object"].split("#")[-1].replace("_", " ").strip()
        pred = rel["predicate"].split("#")[-1].strip()

        # Lưu quan hệ theo hướng Subject → Object
        direct_map[subj].append({
            "predicate": pred,
            "neighbor": obj
        })

    output_path = os.path.join(output_dir, f"{client_name}_direct_map.json")
    # direct_map lúc này là defaultdict(list), chuyển thành dict trước khi xuất
    direct_dict = {k: v for k, v in direct_map.items()}

    import json
    with open(output_path, "w", encoding="utf-8") as fp:
        json.dump(direct_dict, fp, ensure_ascii=False, indent=2)

    print(f"Đã xuất quan hệ trực tiếp của {client_name} ra {output_path}")
