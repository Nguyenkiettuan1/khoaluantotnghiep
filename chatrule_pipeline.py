import os
import json
from datetime import datetime
from typing import List, Dict
from neo4j import GraphDatabase
from openai import OpenAI
from dotenv import load_dotenv

# ====== Cấu hình ======
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
RULES_DIR = "rules"
os.makedirs(RULES_DIR, exist_ok=True)

client = OpenAI(api_key=OPENAI_KEY)

# ====== Khai phá luật ======
class EfficientRuleMiner:
    def __init__(self, uri, user, password, rules_dir="rules"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.rules_dir = rules_dir

    def close(self):
        self.driver.close()

    def extract_2hop_patterns(self, min_support=3):
        """
        Lấy mọi pattern 2-hop phổ biến (theo support) trong KG.
        Trả về list rule và group theo head relation.
        """
        cypher = """
        MATCH (x)-[r1]->(z)-[r2]->(y)
        RETURN type(r1) as r1, type(r2) as r2, type(r2) as head, count(*) as support
        ORDER BY support DESC
        """
        with self.driver.session() as session:
            result = session.run(cypher)
            rules = []
            for record in result:
                if record["support"] >= min_support:
                    rule = f"{record['head']}(X, Y) :- {record['r1']}(X, Z), {record['r2']}(Z, Y)"
                    rules.append({
                        "rule": rule,
                        "head": record['head'],
                        "support": record['support']
                    })
        return rules

    def group_rules_by_head(self, rules):
        grouped = {}
        for r in rules:
            grouped.setdefault(r["head"], []).append(r)
        return grouped

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
            # Chỉ hỗ trợ rule 2-hop cho nhanh (nâng cấp sau)
            if len(body_parts) != 2:
                return {'support': 0, 'confidence': 0, 'pca_confidence': 0}
            p1, p2 = [b.split("(")[0] for b in body_parts]
            cypher = f"""
            MATCH (x)-[:{p1}]->(z)-[:{p2}]->(y)
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

    def run_pipeline(self, min_support=3, n_llm=5, top_k=5):
        # 1. Trích xuất rule 2-hop
        rules_2hop = self.extract_2hop_patterns(min_support)
        grouped = self.group_rules_by_head(rules_2hop)
        print(f"Tìm được {sum(len(v) for v in grouped.values())} rule 2-hop từ KG.")

        # 2. Chạy cho từng head relation
        for rel, rule_list in grouped.items():
            raw_rules = [r["rule"] for r in rule_list]
            print(f"\n==== {rel} ====")
            for r in raw_rules:
                print("Raw:", r)

            # 3. LLM sinh thêm rule
            if len(raw_rules) == 0:
                continue
            new_rules = self.llm_generate_rules(raw_rules, rel, n_new=n_llm)
            all_rules = list(set(raw_rules + new_rules))
            final = self.rank_and_filter_rules(all_rules, top_k=top_k)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.save_results(rel, raw_rules, new_rules, final, timestamp)
            print(f"\nTop-{top_k} rules for {rel}:")
            for x in final:
                print(x)

# ====== MAIN ======
if __name__ == "__main__":
    miner = EfficientRuleMiner(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    miner.run_pipeline(min_support=3, n_llm=5, top_k=5)
    miner.close()
