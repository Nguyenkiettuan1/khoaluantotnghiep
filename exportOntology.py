from neo4j import GraphDatabase

# Kết nối đến Neo4j
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "123456789"))

def get_all_nodes(tx):
    # Sử dụng coalesce để lấy giá trị của thuộc tính "name" nếu tồn tại, nếu không sử dụng id(n)
    query = """
    MATCH (n)
    RETURN DISTINCT coalesce(n['name'], toString(id(n))) AS name, labels(n) AS labels
    """
    result = tx.run(query)
    # Trả về dict: tên node -> danh sách labels
    return {record["name"]: record["labels"] for record in result if record["name"]}

def get_all_relationships(tx):
    # Tương tự, sử dụng coalesce cho các node nguồn và đích
    query = """
    MATCH (n)-[r]->(m)
    RETURN coalesce(n['name'], toString(id(n))) AS source, 
           type(r) AS rel, 
           coalesce(m['name'], toString(id(m))) AS target
    """
    result = tx.run(query)
    return [{"source": record["source"], "rel": record["rel"], "target": record["target"]}
            for record in result if record["source"] and record["target"]]

with driver.session(database="sgugemini") as session:
    nodes = session.execute_read(get_all_nodes)
    relationships = session.execute_read(get_all_relationships)

driver.close()

# Tạo dictionary cho properties: key = relationship type, value = (set(domain), set(range))
properties = {}
for rel in relationships:
    rel_type = rel['rel']
    src = rel['source']
    tgt = rel['target']
    if rel_type not in properties:
        properties[rel_type] = (set(), set())
    properties[rel_type][0].add(src)
    properties[rel_type][1].add(tgt)

# Xuất dữ liệu ra file TTL theo chuẩn với cấu trúc:
# - Các prefix theo yêu cầu
# - # Classes: liệt kê các node dưới dạng rdfs:Class
# - # Properties: liệt kê các quan hệ dưới dạng rdf:Property với domain và range
# - # Relationships: liệt kê các triple (instance) quan hệ
with open("./ontology/sgugemini.ttl", "w", encoding="utf-8") as f:
    # Ghi các prefix theo yêu cầu
    f.write("@prefix : <http://example.org/sgu#> .\n")
    f.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
    f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
    f.write("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n\n")
    
    # Định nghĩa ontology chung
    f.write("<http://example.org/sgu> a owl:Ontology .\n\n")
    
    # # Classes
    f.write("# Classes\n")
    for name, lbls in nodes.items():
        f.write(f":{name} a rdfs:Class .\n")
    f.write("\n")
    
    # # Properties
    f.write("# Properties\n")
    for prop, (domains, ranges) in properties.items():
        domain_str = ", ".join(f":{d}" for d in sorted(domains))
        range_str = ", ".join(f":{r}" for r in sorted(ranges))
        f.write(f":{prop} a rdf:Property ;\n")
        f.write(f"    rdfs:domain {domain_str} ;\n")
        f.write(f"    rdfs:range {range_str} .\n\n")
    
    # # Relationships (instance data)
    f.write("# Relationships\n")
    for rel in relationships:
        f.write(f":{rel['source']} :{rel['rel']} :{rel['target']} .\n")

print("Ontology đã được trích xuất và lưu vào file extracted_ontology.ttl")
