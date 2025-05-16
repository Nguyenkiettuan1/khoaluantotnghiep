import os
import random
import json
from datetime import datetime
from typing import List, Dict
from neo4j import GraphDatabase
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv('OPENAI_API_KEY')
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
RULES_DIR = "rules"
os.makedirs(RULES_DIR, exist_ok=True)

client = OpenAI(api_key=OPENAI_KEY)

class EfficientRuleMiner:
    def __init__(self, uri, user, password, max_path_len=3, rules_dir="rules"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.max_path_len = max_path_len
        self.rules_dir = rules_dir

    def close(self):
        self.driver.close()

    def get_all_relations(self) -> list:
        with self.driver.session() as session:
            result = session.run("CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType")
            return [r['relationshipType'] for r in result]

    def get_sample_triples(self, rel: str, k=10) -> List[Dict]:
        # Dùng elementId thay vì id
        query = f"""
        MATCH (x)-[r:`{rel}`]->(y)
        RETURN elementId(x) AS xid, elementId(y) AS yid
        LIMIT {k*5}
        """
        with self.driver.session() as session:
            result = session.run(query)
            edges = [dict(r) for r in result]
            return random.sample(edges, min(k, len(edges)))

    def get_2hop_paths(self, rel: str, triples: List[Dict], per_pair=3) -> List[str]:
        """Tìm luật thô (2-hop path) từ cặp triple."""
        rules = []
        with self.driver.session() as session:
            for pair in triples:
                query = f"""
                MATCH (x)-[p1]->(z)-[p2]->(y)
                WHERE elementId(x) = $xid AND elementId(y) = $yid
                  AND type(p1) <> $rel AND type(p2) <> $rel
                  AND x <> y AND x <> z AND y <> z
                RETURN DISTINCT type(p1) AS r1, type(p2) AS r2
                LIMIT {per_pair}
                """
                result = session.run(query, xid=pair['xid'], yid=pair['yid'], rel=rel)
                for rec in result:
                    rule = f"{rel}(X,Y) :- {rec['r1']}(X,Z), {rec['r2']}(Z,Y)"
                    rules.append(rule)
        return rules

    # Optionally: thử cả 3-hop nếu 2-hop quá ít luật
    def get_3hop_paths(self, rel: str, triples: List[Dict], per_pair=2) -> List[str]:
        rules = []
        with self.driver.session() as session:
            for pair in triples:
                query = f"""
                MATCH (x)-[p1]->(a)-[p2]->(b)-[p3]->(y)
                WHERE elementId(x) = $xid AND elementId(y) = $yid
                  AND ALL(t IN [type(p1), type(p2), type(p3)] WHERE t <> $rel)
                  AND x <> y AND x <> a AND x <> b AND y <> a AND y <> b AND a <> b
                RETURN DISTINCT type(p1) AS r1, type(p2) AS r2, type(p3) AS r3
                LIMIT {per_pair}
                """
                result = session.run(query, xid=pair['xid'], yid=pair['yid'], rel=rel)
                for rec in result:
                    rule = f"{rel}(X,Y) :- {rec['r1']}(X,A), {rec['r2']}(A,B), {rec['r3']}(B,Y)"
                    rules.append(rule)
        return rules

    def llm_generate_rules(self, rules: List[str], rel: str, n_new=5) -> List[str]:
        prompt = f"""You are an expert in logical reasoning and knowledge graphs.
Below are {len(rules)} example rules for the relation "{rel}":
{chr(10).join(rules)}
Please generate {n_new} new logical rules for the relation "{rel}" in the same syntax (head(X,Y) :- body1(X,Z), body2(Z,Y)), with no explanation and no duplicates."""
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a knowledge graph reasoning expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=512,
            temperature=0.8
        )
        new_rules = [l.strip() for l in response.choices[0].message.content.strip().split("\n") if ":-" in l]
        return new_rules

    def calc_support_confidence(self, rule: str) -> Dict:
        try:
            head, body = rule.split(":-")
            head_pred, _ = head.strip().split("(")
            body_parts = [b.strip() for b in body.strip().split(",")]
            # Hỗ trợ cả 2-hop và 3-hop rule
            p_rels = [b.split("(")[0] for b in body_parts]
            var_list = ['Z', 'A', 'B']
            match_str = ""
            # Tạo pattern Cypher theo số hop
            if len(p_rels) == 2:
                match_str = f"(x)-[:{p_rels[0]}]->(z)-[:{p_rels[1]}]->(y)"
            elif len(p_rels) == 3:
                match_str = f"(x)-[:{p_rels[0]}]->(a)-[:{p_rels[1]}]->(b)-[:{p_rels[2]}]->(y)"
            else:
                return {'support': 0, 'confidence': 0, 'pca_confidence': 0}
            cypher = f"""
            MATCH {match_str}
            OPTIONAL MATCH (x)-[r:{head_pred}]->(y)
            WITH x, y, COUNT(r) AS head_exists
            RETURN count(*) AS body_total, sum(CASE WHEN head_exists > 0 THEN 1 ELSE 0 END) AS support
            """
            with self.driver.session() as session:
                result = session.run(cypher).single()
                support = result['support']
                body_total = result['body_total']
                confidence = (support / body_total) if body_total > 0 else 0
                return {
                    'support': support,
                    'confidence': confidence,
                    'pca_confidence': confidence  # simple version
                }
        except Exception as e:
            print(f"Rule error: {rule} - {e}")
            return {'support': 0, 'confidence': 0, 'pca_confidence': 0}

    def rank_and_filter_rules(self, rules: List[str], top_k=5) -> List[Dict]:
        scored = []
        for rule in rules:
            metrics = self.calc_support_confidence(rule)
            if metrics['support'] > 0:
                scored.append({'rule': rule, **metrics})
        scored = sorted(scored, key=lambda x: x['pca_confidence'], reverse=True)
        return scored[:top_k]

    def save_results(self, rel: str, raw_rules: List[str], new_rules: List[str], final_rules: List[Dict], timestamp: str):
        results_dir = os.path.join(self.rules_dir, timestamp)
        os.makedirs(results_dir, exist_ok=True)

        raw_file = os.path.join(results_dir, f"{rel}_raw_rules.json")
        with open(raw_file, "w", encoding="utf-8") as f:
            json.dump({
                "relation": rel,
                "timestamp": timestamp,
                "rules": raw_rules
            }, f, indent=2, ensure_ascii=False)

        new_file = os.path.join(results_dir, f"{rel}_new_rules.json")
        with open(new_file, "w", encoding="utf-8") as f:
            json.dump({
                "relation": rel,
                "timestamp": timestamp,
                "rules": new_rules
            }, f, indent=2, ensure_ascii=False)

        final_file = os.path.join(results_dir, f"{rel}_final_rules.json")
        with open(final_file, "w", encoding="utf-8") as f:
            json.dump({
                "relation": rel,
                "timestamp": timestamp,
                "rules": final_rules
            }, f, indent=2, ensure_ascii=False)

        summary_file = os.path.join(results_dir, f"{rel}_summary.txt")
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(f"Rule Mining Summary for relation: {rel}\n")
            f.write(f"Timestamp: {timestamp}\n\n")
            f.write(f"Raw Rules: {len(raw_rules)}\n")
            f.write(f"New Rules from LLM: {len(new_rules)}\n")
            f.write(f"Final Rules: {len(final_rules)}\n\n")
            f.write("Top Rules:\n")
            for i, rule in enumerate(final_rules, 1):
                f.write(f"\n{i}. Rule: {rule['rule']}\n")
                f.write(f"   Support: {rule['support']}\n")
                f.write(f"   Confidence: {rule['confidence']:.3f}\n")
                f.write(f"   PCA-Confidence: {rule['pca_confidence']:.3f}\n")

        print(f"\nResults saved in directory: {results_dir}")
        print(f"- Raw rules: {raw_file}")
        print(f"- New rules: {new_file}")
        print(f"- Final rules: {final_file}")
        print(f"- Summary: {summary_file}")

    def run(self, rel: str, k_samples=10, n_llm=5, top_k=5):
        triples = self.get_sample_triples(rel, k_samples)
        raw_rules = self.get_2hop_paths(rel, triples)
        # Nếu 2-hop quá ít, thử sinh 3-hop rule
        if len(raw_rules) < 3:
            raw_rules += self.get_3hop_paths(rel, triples)
        if not raw_rules:
            print(f"No path-based rules found for {rel}")
            return []
        new_rules = self.llm_generate_rules(raw_rules, rel, n_new=n_llm)
        all_rules = list(set(raw_rules + new_rules))
        final = self.rank_and_filter_rules(all_rules, top_k)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.save_results(rel, raw_rules, new_rules, final, timestamp)
        print(f"\nTop-{top_k} rules for {rel}:")
        for x in final:
            print(x)
        return final

if __name__ == "__main__":
    miner = EfficientRuleMiner(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    all_rels = miner.get_all_relations()
    print(f"\nAll relations in KG: {all_rels}")
    skip_rels = ['owl__sameAs', 'rdfs__subClassOf', 'rdf__type']
    filtered_rels = [r for r in all_rels if r not in skip_rels]
    for rel in filtered_rels:
        miner.run(rel, k_samples=10, n_llm=5, top_k=5)
    miner.close()
