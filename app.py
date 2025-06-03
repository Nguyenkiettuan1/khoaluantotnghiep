import streamlit as st
import os
from typing import List, Optional, Dict
from dotenv import load_dotenv
from neo4jconnector import Neo4jConnection, Neo4jVectorSearchError
import logging
from dataclasses import dataclass
import pandas as pd
from collections import defaultdict, deque


# Load environment variables
load_dotenv()

# Configure page
st.set_page_config("SGU Vector Chatbot", page_icon="🎓", layout="centered")

# Initialize logger
logger = logging.getLogger('neo4j_vector_search')

@dataclass
class SearchResult:
    """Class to represent a search result"""
    name: str
    node_type: str
    similarity: float
    description: Optional[str] = None

def init_neo4j_clients() -> Dict[str, Dict]:
    cfg = {
        "uri": os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        "user": os.getenv("NEO4J_USER", "neo4j"),
        "password": os.getenv("NEO4J_PASSWORD"),
    }

    return {
        "deepseek": {
            "conn": Neo4jConnection(**cfg, dbname="deepseek"),
            "label_file": "labels/neo4j_labels_deepseek.txt",
        },
        "gemini": {
            "conn": Neo4jConnection(**cfg, dbname="gemini"),
            "label_file": "labels/neo4j_labels_gemini.txt",
        },
        "openai": {
            "conn": Neo4jConnection(**cfg, dbname="openai"),
            "label_file": "labels/neo4j_labels_openai.txt",
        },
    }

def find_indirect_paths(graph: Dict, start: str, targets: set, max_depth: int = 3):
    """Tìm các đường vòng từ thực thể đến target"""
    paths = []
    queue = deque([(start, [], set())])
    while queue:
        node, path, visited = queue.popleft()
        if len(path) > max_depth:
            continue
        for neighbor, rel in graph.get(node, []):
            if neighbor in visited:
                continue
            new_path = path + [(node, rel, neighbor)]
            if neighbor in targets:
                paths.append(new_path)
            else:
                queue.append((neighbor, new_path, visited | {neighbor}))
    return paths

def build_relation_graph(relations: List[Dict]) -> Dict[str, List[tuple]]:
    """Xây đồ thị từ các quan hệ ontology"""
    graph = defaultdict(list)
    for rel in relations:
        subj = rel["subject"].split("#")[-1].replace("_", " ").strip()
        obj = rel["object"].split("#")[-1].replace("_", " ").strip()
        pred = rel["predicate"].split("#")[-1].strip()
        graph[subj].append((obj, pred))
    return graph


def perform_search(neo4j: Neo4jConnection, query: str, node_types: List[str], min_similarity: float = 0.5, limit: int = 20) -> List[Dict]:
    """Perform vector search across specified node types"""
    all_results = []
    
    try:
        for node_type in node_types:
            # Search for each node type
            results = neo4j.similarity_search(
                query_text=query,
                node_label=node_type,
                limit=limit,
                min_similarity=min_similarity
            )
            
            # Add node type to results
            for result in results:
                result['node_type'] = node_type
            
            all_results.extend(results)
                
    except Exception as e:
        logger.error(f"Error performing search: {e}")
        st.error(f"Error performing search: {str(e)}")
    
    return sorted(all_results, key=lambda x: x['similarity'], reverse=True)

    
def extract_labels_from_file(file_path: str) -> List[str]:
    """Extract labels from a file and return as a list"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            labels = [label.strip() for label in f.read().splitlines() if label.strip()]
        return labels
    except Exception as e:
        logger.error(f"Error reading labels from file: {e}")
        st.error(f"Error reading labels from file: {str(e)}")
        return []
def get_answer_from_search_results(neo4j: Neo4jConnection, userQuery: str, labels: List[str]) -> Optional[str]:
    """Get answer from search results using OpenAI API"""
    try:
        # Perform search
        search_results = perform_search(neo4j, userQuery, labels, min_similarity=0.6, limit=30)
        
        if search_results:
            # Generate answer
            answer = neo4j.generate_answer(neo4j, userQuery, search_results)
            return answer
        else:
            st.info("Không tìm thấy kết quả phù hợp với tiêu chí của bạn")
            return None
    except Exception as e:
        logger.error(f"Error getting answer: {e}")
        st.error(f"Error getting answer: {str(e)}")
        return None

@st.cache_data(show_spinner=False)
def load_labels(path: str) -> List[str]:
    with open(path, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]


@st.cache_data(show_spinner=False)
def load_ontology_relations(client_name: str) -> List[Dict]:
    """Load ontology relations tương ứng với client đã chọn"""
    path_map = {
        "deepseek": "ontology_relations_deepseek.csv",
        "gemini": "ontology_relations_gemini.csv",
        "openai": "ontology_relations_openai.csv"
    }
    path = path_map.get(client_name)
    if not path or not os.path.exists(path):
        return []

    df = pd.read_csv(path)
    return df.to_dict(orient="records")
 
# # ─── main.py (phần quan trọng) ─────────────────────────────────────────────
# def main() -> None:
#     st.title("SGU Vector Search 🔍")
    
#     # 1) Chọn client
#     clients = init_neo4j_clients()
#     client_name = st.sidebar.selectbox("🔧 Chọn mô hình", list(clients))
#     neo4j_cfg = clients[client_name]
#     neo4j = neo4j_cfg["conn"]
#     labels = load_labels(neo4j_cfg["label_file"])     # ⚠ tất cả label hiện có
    
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []


#     # 2) Nhập truy vấn + tham số
#     q = st.text_input("Nhập câu hỏi của bạn")
#     col1, col2 = st.columns(2)
#     with col1:
#         min_sim = st.slider("Độ tương đồng tối thiểu", 0.0, 1.0, 0.5, 0.05)
#     with col2:
#         limit = st.slider("Kết quả tối đa", 1, 20, 10)

#     # 3) Luôn tìm trên toàn bộ label
#     node_types = labels                            # ← không còn chọn lọc

#     # 4) Thực thi tìm kiếm
#     if q.strip():
#         with st.spinner("Đang tìm kiếm..."):
#             results = perform_search(neo4j, q, node_types, min_sim, limit)

#         if not results:
#             st.warning("Không tìm thấy kết quả.")
#             return

#     # 🧠 Load các quan hệ từ ontology
#         ontology_relations = load_ontology_relations(client_name)
        
#                 # Build graph and enrich relations if needed
#         names = set(r["name"] for r in results)
#         graph = build_relation_graph(ontology_relations)

#         # Tìm quan hệ trực tiếp
#         related_relations = []
#         direct_found = False
#         for rel in ontology_relations:
#             subj = rel["subject"].split("#")[-1].replace("_", " ")
#             obj = rel["object"].split("#")[-1].replace("_", " ")
#             pred = rel["predicate"].split("#")[-1]
#             if subj in names or obj in names:
#                 related_relations.append(f"{subj} → {pred} → {obj}")
#                 direct_found = True

#         # Nếu không có quan hệ trực tiếp, tìm đường vòng
#         if not direct_found:
#             for name in names:
#                 paths = find_indirect_paths(graph, name, names)
#                 for path in paths:
#                     sentence = " → ".join([f"{s} --{r}→ {o}" for s, r, o in path])
#                     related_relations.append(f"Đường vòng: {sentence}")
#         answer = None
#         # Truyền quan hệ vào generate_answer
#         with st.spinner("Đang tạo câu trả lời..."):
#             chat_history = st.session_state.chat_history.copy()
            
#             answer = neo4j.generate_answer(q, results, ontology_relations=ontology_relations, chat_history=chat_history)

#         st.subheader("📝 Câu trả lời")
#         st.write(answer or "Không sinh được câu trả lời.")
        
        
#         if answer:
#             st.session_state.chat_history.append({"role": "user", "content": q})
#             st.session_state.chat_history.append({"role": "assistant", "content": answer})
        
#         with st.expander("💬 Lịch sử hội thoại trước đó", expanded=True):
#             for msg in st.session_state.chat_history:
#                 if msg["role"] == "user":
#                     st.markdown(f"🧑 **Bạn:** {msg['content']}")
#                 elif msg["role"] == "assistant":
#                     st.markdown(f"🤖 **Trợ lý:** {msg['content']}")
                                
#         with st.expander("🔎 Chi tiết kết quả"):
#             for r in results:
#                 st.markdown(
#                     f"**{r['name']}** ({r['node_type']}) — "
#                     f"Similarity: `{r['similarity']:.4f}`"
#                 )
#                 if desc := r.get("description"):
#                     st.write(desc)
#                 st.divider()


def main():
        st.title("🎓 Trợ lý Chatbot SGU")

        # Khởi tạo state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "last_results" not in st.session_state:
            st.session_state.last_results = []

        # Chọn mô hình
        clients = init_neo4j_clients()
        client_name = st.sidebar.selectbox("🔧 Chọn mô hình", list(clients))
        neo4j_cfg = clients[client_name]
        neo4j = neo4j_cfg["conn"]
        labels = load_labels(neo4j_cfg["label_file"])
        ontology_relations = load_ontology_relations(client_name)

        # Các tuỳ chọn tìm kiếm
        col1, col2 = st.columns(2)
        with col1:
            min_sim = st.slider("Độ tương đồng tối thiểu", 0.0, 1.0, 0.5, 0.05)
        with col2:
            limit = st.slider("Kết quả tối đa", 1, 20, 10)

        # Hiển thị hội thoại cũ
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Input chat
        prompt = st.chat_input("Nhập câu hỏi...")

        if prompt:
            # Hiển thị user chat
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.chat_history.append({"role": "user", "content": prompt})

            with st.spinner("🔎 Đang tìm kiếm..."):
                results = perform_search(neo4j, prompt, labels, min_similarity=min_sim, limit=limit)
                st.session_state.last_results = results

            # Nếu không có kết quả
            if not results:
                response_text = "Không tìm thấy kết quả phù hợp."
                with st.chat_message("assistant"):
                    st.markdown(response_text)
                st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                return

            # Build graph & liên kết
            names = set(r["name"] for r in results)
            graph = build_relation_graph(ontology_relations)
            related_relations = []

            for rel in ontology_relations:
                subj = rel["subject"].split("#")[-1].replace("_", " ")
                obj = rel["object"].split("#")[-1].replace("_", " ")
                pred = rel["predicate"].split("#")[-1]
                if subj in names or obj in names:
                    related_relations.append(f"{subj} → {pred} → {obj}")

            if not related_relations:
                for name in names:
                    paths = find_indirect_paths(graph, name, names)
                    for path in paths:
                        sentence = " → ".join([f"{s} --{r}→ {o}" for s, r, o in path])
                        related_relations.append(f"Đường vòng: {sentence}")

            # Sinh câu trả lời
            with st.chat_message("assistant"):
                with st.spinner("🤖 Trợ lý đang trả lời..."):
                    chat_history_copy = st.session_state.chat_history.copy()
                    response_text = neo4j.generate_answer(
                        prompt, results, ontology_relations=ontology_relations, chat_history=chat_history_copy
                    )
                    st.markdown(response_text)
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})

            # ✅ Hiển thị kết quả chi tiết
            with st.expander("🔎 Chi tiết kết quả"):
                for r in results:
                    st.markdown(
                        f"**{r['name']}** ({r['node_type']}) — "
                        f"Similarity: `{r['similarity']:.4f}`"
                    )
                    if desc := r.get("description"):
                        st.write(desc)
                    st.divider()

        # Nút xóa hội thoại
        if st.sidebar.button("🧹 Xoá hội thoại"):
            st.session_state.chat_history = []
            st.session_state.last_results = []
            st.rerun()

if __name__ == "__main__":
    main()
    