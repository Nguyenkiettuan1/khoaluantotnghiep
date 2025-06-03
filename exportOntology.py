# from neo4j import GraphDatabase
# import re
# database = 'openai'
# def sanitize_unicode(name: str) -> str:
#     # Giữ Unicode letters & digits, thay ký tự khác thành '_'
#     s = re.sub(r'[^\w]', '_', name)
#     if re.match(r'^\d', s):
#         s = '_' + s
#     return s

# # Kết nối Neo4j
# driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j","123456789"))

# def get_nodes(tx):
#     return [
#         {"name": r["name"], "desc": r["description"]}
#         for r in tx.run(
#             """
#             MATCH (n)
#             WHERE n.name IS NOT NULL
#             RETURN DISTINCT
#               n.name        AS name,
#               coalesce(n.description, '') AS description
#             """
#         )
#     ]

# def get_rels(tx):
#     return [
#         {"s": r["source"], "p": r["rel"], "o": r["target"]}
#         for r in tx.run(
#             """
#             MATCH (n)-[r]->(m)
#             WHERE n.name IS NOT NULL AND m.name IS NOT NULL
#             RETURN
#               n.name    AS source,
#               type(r)   AS rel,
#               m.name    AS target
#             """
#         )
#     ]

# with driver.session(database=database) as sess:
#     raw_nodes = sess.execute_read(get_nodes)
#     raw_rels  = sess.execute_read(get_rels)
# driver.close()

# # Map và props
# nodes = { item["name"]: sanitize_unicode(item["name"]) for item in raw_nodes }
# descs = { item["name"]: item["desc"].replace('"','\\"') for item in raw_nodes }
# props = {}
# for r in raw_rels:
#     p = sanitize_unicode(r["p"])
#     props.setdefault(p, {"orig": r["p"], "domains": set(), "ranges": set()})
#     props[p]["domains"].add(sanitize_unicode(r["s"]))
#     props[p]["ranges"].add(sanitize_unicode(r["o"]))

# with open(f"./ontology/{database}.ttl","w",encoding="utf-8") as f:
#     # Prefixes
#     f.write("@prefix :    <http://example.org/sgu#> .\n")
#     f.write("@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
#     f.write("@prefix owl:  <http://www.w3.org/2002/07/owl#> .\n")
#     f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n")

#     # Ontology header
#     f.write(":SGU rdf:type owl:Ontology .\n")
#     f.write(f":SGU rdfs:label \"DeepSeek Ontology\"@en .\n")
#     f.write(f":SGU rdfs:comment \"Ontology trích xuất từ Neo4j\"@en .\n\n")

#     # Classes
#     f.write("# Classes\n")
#     for orig, clean in sorted(nodes.items(), key=lambda x: x[1]):
#         f.write(f":{clean} rdf:type owl:Class .\n")
#         f.write(f":{clean} rdfs:label \"{orig}\"@vi .\n")
#         f.write(f":{clean} rdfs:comment \"{descs[orig]}\"@vi .\n")
#     f.write("\n")

#     # Object Properties
#     f.write("# Object Properties\n")
#     for clean, info in sorted(props.items()):
#         f.write(f":{clean} rdf:type owl:ObjectProperty .\n")
#         f.write(f":{clean} rdfs:label \"{info['orig']}\"@en .\n")
#         for d in sorted(info["domains"]):
#             f.write(f":{clean} rdfs:domain :{d} .\n")
#         for r_ in sorted(info["ranges"]):
#             f.write(f":{clean} rdfs:range :{r_} .\n")
#     f.write("\n")

#     # Instance data
#     f.write("# Relationships\n")
#     for r in raw_rels:
#         s = sanitize_unicode(r["s"])
#         p = sanitize_unicode(r["p"])
#         o = sanitize_unicode(r["o"])
#         f.write(f":{s} :{p} :{o} .\n")

# print(f"Đã tạo {database}.ttl – bạn hãy import file này vào Protégé.")

from neo4j import GraphDatabase
import os
import re

def sanitize_unicode(name: str) -> str:
    """Chuyển tên thành định dạng an toàn cho RDF (giữ Unicode, thay ký tự lạ bằng _)"""
    s = re.sub(r'[^\w]', '_', name)
    return '_' + s if re.match(r'^\d', s) else s

def export_neo4j_to_ttl(databases: list, uri="bolt://localhost:7687", auth=("neo4j", "123456789")):
    driver = GraphDatabase.driver(uri, auth=auth)

    def get_nodes(tx):
        return [
            {"name": r["name"], "desc": r["description"]}
            for r in tx.run("""
                MATCH (n)
                WHERE n.name IS NOT NULL
                RETURN DISTINCT
                    n.name AS name,
                    coalesce(n.description, '') AS description
            """)
        ]

    def get_rels(tx):
        return [
            {"s": r["source"], "p": r["rel"], "o": r["target"]}
            for r in tx.run("""
                MATCH (n)-[r]->(m)
                WHERE n.name IS NOT NULL AND m.name IS NOT NULL
                RETURN
                    n.name  AS source,
                    type(r) AS rel,
                    m.name  AS target
            """)
        ]

    os.makedirs("ontology", exist_ok=True)

    for db in databases:
        with driver.session(database=db) as sess:
            raw_nodes = sess.execute_read(get_nodes)
            raw_rels = sess.execute_read(get_rels)

        nodes = {item["name"]: sanitize_unicode(item["name"]) for item in raw_nodes}
        descs = {item["name"]: item["desc"].replace('"', '\\"') for item in raw_nodes}

        props = {}
        for r in raw_rels:
            p = sanitize_unicode(r["p"])
            props.setdefault(p, {"orig": r["p"], "domains": set(), "ranges": set()})
            props[p]["domains"].add(sanitize_unicode(r["s"]))
            props[p]["ranges"].add(sanitize_unicode(r["o"]))

        ttl_path = f"./ontology/{db}.ttl"
        with open(ttl_path, "w", encoding="utf-8") as f:
            f.write("@prefix :    <http://example.org/sgu#> .\n")
            f.write("@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
            f.write("@prefix owl:  <http://www.w3.org/2002/07/owl#> .\n")
            f.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\n")

            f.write(f":SGU rdf:type owl:Ontology .\n")
            f.write(f":SGU rdfs:label \"{db} Ontology\"@en .\n")
            f.write(f":SGU rdfs:comment \"Ontology trích xuất từ Neo4j database '{db}'\"@en .\n\n")

            f.write("# Classes\n")
            for orig, clean in sorted(nodes.items(), key=lambda x: x[1]):
                f.write(f":{clean} rdf:type owl:Class .\n")
                f.write(f":{clean} rdfs:label \"{orig}\"@vi .\n")
                f.write(f":{clean} rdfs:comment \"{descs[orig]}\"@vi .\n")
            f.write("\n")

            f.write("# Object Properties\n")
            for clean, info in sorted(props.items()):
                f.write(f":{clean} rdf:type owl:ObjectProperty .\n")
                f.write(f":{clean} rdfs:label \"{info['orig']}\"@en .\n")
                for d in sorted(info["domains"]):
                    f.write(f":{clean} rdfs:domain :{d} .\n")
                for r_ in sorted(info["ranges"]):
                    f.write(f":{clean} rdfs:range :{r_} .\n")
            f.write("\n")

            f.write("# Relationships\n")
            for r in raw_rels:
                s = sanitize_unicode(r["s"])
                p = sanitize_unicode(r["p"])
                o = sanitize_unicode(r["o"])
                f.write(f":{s} :{p} :{o} .\n")

        print(f"✔ Đã tạo file {ttl_path} với {len(raw_nodes)} lớp và {len(raw_rels)} quan hệ.")

    driver.close()

export_neo4j_to_ttl(["openai", "gemini", "deepseek"])
