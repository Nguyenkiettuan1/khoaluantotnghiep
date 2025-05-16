from neo4j import GraphDatabase
import re
database = 'openai'
def sanitize_unicode(name: str) -> str:
    # Giữ Unicode letters & digits, thay ký tự khác thành '_'
    s = re.sub(r'[^\w]', '_', name)
    if re.match(r'^\d', s):
        s = '_' + s
    return s

# Kết nối Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j","123456789"))

def get_nodes(tx):
    return [
        {"name": r["name"], "desc": r["description"]}
        for r in tx.run(
            """
            MATCH (n)
            WHERE n.name IS NOT NULL
            RETURN DISTINCT
              n.name        AS name,
              coalesce(n.description, '') AS description
            """
        )
    ]

def get_rels(tx):
    return [
        {"s": r["source"], "p": r["rel"], "o": r["target"]}
        for r in tx.run(
            """
            MATCH (n)-[r]->(m)
            WHERE n.name IS NOT NULL AND m.name IS NOT NULL
            RETURN
              n.name    AS source,
              type(r)   AS rel,
              m.name    AS target
            """
        )
    ]

with driver.session(database=database) as sess:
    raw_nodes = sess.execute_read(get_nodes)
    raw_rels  = sess.execute_read(get_rels)
driver.close()

# Map và props
nodes = { item["name"]: sanitize_unicode(item["name"]) for item in raw_nodes }
descs = { item["name"]: item["desc"].replace('"','\\"') for item in raw_nodes }
props = {}
for r in raw_rels:
    p = sanitize_unicode(r["p"])
    props.setdefault(p, {"orig": r["p"], "domains": set(), "ranges": set()})
    props[p]["domains"].add(sanitize_unicode(r["s"]))
    props[p]["ranges"].add(sanitize_unicode(r["o"]))

with open(f"{database}.ttl","w",encoding="utf-8") as f:
    # Prefixes
    f.write("@prefix :    <http://example.org/sgu#> .\n")
    f.write("@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
    f.write("@prefix owl:  <http://www.w3.org/2002/07/owl#> .\n")
    f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n")

    # Ontology header
    f.write(":SGU rdf:type owl:Ontology .\n")
    f.write(f":SGU rdfs:label \"DeepSeek Ontology\"@en .\n")
    f.write(f":SGU rdfs:comment \"Ontology trích xuất từ Neo4j\"@en .\n\n")

    # Classes
    f.write("# Classes\n")
    for orig, clean in sorted(nodes.items(), key=lambda x: x[1]):
        f.write(f":{clean} rdf:type owl:Class .\n")
        f.write(f":{clean} rdfs:label \"{orig}\"@vi .\n")
        f.write(f":{clean} rdfs:comment \"{descs[orig]}\"@vi .\n")
    f.write("\n")

    # Object Properties
    f.write("# Object Properties\n")
    for clean, info in sorted(props.items()):
        f.write(f":{clean} rdf:type owl:ObjectProperty .\n")
        f.write(f":{clean} rdfs:label \"{info['orig']}\"@en .\n")
        for d in sorted(info["domains"]):
            f.write(f":{clean} rdfs:domain :{d} .\n")
        for r_ in sorted(info["ranges"]):
            f.write(f":{clean} rdfs:range :{r_} .\n")
    f.write("\n")

    # Instance data
    f.write("# Relationships\n")
    for r in raw_rels:
        s = sanitize_unicode(r["s"])
        p = sanitize_unicode(r["p"])
        o = sanitize_unicode(r["o"])
        f.write(f":{s} :{p} :{o} .\n")

print(f"Đã tạo {database}.ttl – bạn hãy import file này vào Protégé.")
