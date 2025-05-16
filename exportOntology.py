from neo4j import GraphDatabase
import re

# Hàm sanitize_unicode:
# - Thay mọi ký tự không phải chữ/ số/ gạch dưới thành '_'
# - Nhưng vẫn giữ nguyên các ký tự Unicode (kể cả tiếng Việt có dấu)
# - Nếu kết quả bắt đầu bằng số thì thêm '_' vào trước
def sanitize_unicode(name: str) -> str:
    # \w trong Python RE theo default đã bao gồm Unicode letters & digits
    s = re.sub(r'[^\w]', '_', name)
    if re.match(r'^\d', s):
        s = '_' + s
    return s

# Kết nối đến Neo4j
uri    = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "123456789"))

def get_all_nodes(tx):
    q = """
    MATCH (n)
    RETURN DISTINCT coalesce(n.name, toString(id(n))) AS name
    """
    return [r["name"] for r in tx.run(q)]

def get_all_relationships(tx):
    q = """
    MATCH (n)-[r]->(m)
    RETURN
      coalesce(n.name, toString(id(n))) AS source,
      type(r)                         AS rel,
      coalesce(m.name, toString(id(m))) AS target
    """
    return [dict(r) for r in tx.run(q)]

# Đọc dữ liệu
with driver.session(database="deepseek") as sess:
    raw_nodes = sess.read_transaction(get_all_nodes)
    raw_rels  = sess.read_transaction(get_all_relationships)
driver.close()

# Ánh xạ tên gốc -> tên sanitize (giữ dấu Tiếng Việt)
nodes_map = {orig: sanitize_unicode(orig) for orig in raw_nodes}

# Gom domains & ranges cho mỗi loại quan hệ
props = {}
for r in raw_rels:
    p   = sanitize_unicode(r['rel'])
    s   = sanitize_unicode(r['source'])
    t   = sanitize_unicode(r['target'])
    props.setdefault(p, {'orig': r['rel'], 'domains': set(), 'ranges': set()})
    props[p]['domains'].add(s)
    props[p]['ranges'].add(t)

# Viết file TTL
with open("extracted_ontology.ttl", "w", encoding="utf-8") as f:
    # Prefix
    f.write("@prefix :    <http://example.org/sgu#> .\n")
    f.write("@prefix owl:  <http://www.w3.org/2002/07/owl#> .\n")
    f.write("@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
    f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n")

    # Ontology header
    f.write(":SGU a owl:Ontology ;\n")
    f.write("    rdfs:label   \"SGU Ontology\"@en ;\n")
    f.write("    rdfs:comment \"Ontology trích xuất từ Neo4j\"@en .\n\n")

    # Classes với rdfs:label giữ nguyên tên Tiếng Việt
    f.write("# Classes\n")
    for orig, clean in sorted(nodes_map.items(), key=lambda x: x[1]):
        f.write(f":{clean} a owl:Class ;\n")
        f.write(f"    rdfs:label \"{orig}\"@vi .\n")
    f.write("\n")

    # Object Properties với rdfs:label giữ nguyên rel type
    f.write("# Object Properties\n")
    for clean, dr in sorted(props.items()):
        f.write(f":{clean} a owl:ObjectProperty ;\n")
        f.write(f"    rdfs:label \"{dr['orig']}\"@en ;\n")
        # mỗi domain / range là một triple riêng
        for d in sorted(dr['domains']):
            f.write(f"    rdfs:domain :{d} ;\n")
        for r_ in sorted(dr['ranges']):
            f.write(f"    rdfs:range  :{r_} ;\n")
        # xóa dấu ';' cuối và thêm '.'
        f.seek(f.tell() - 2)
        f.write(".\n\n")

    # Instance data (giữ nguyên label đã sanitize_unicode)
    f.write("# Relationships (instance data)\n")
    for r in raw_rels:
        s = sanitize_unicode(r['source'])
        p = sanitize_unicode(r['rel'])
        t = sanitize_unicode(r['target'])
        f.write(f":{s} :{p} :{t} .\n")

print("Đã tạo xong extracted_ontology.ttl — import vào Protégé sẽ hiển thị đúng Tiếng Việt.") 
