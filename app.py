import streamlit as st
import os
from typing import List, Optional, Dict
from dotenv import load_dotenv
from neo4jconnector import Neo4jConnection, Neo4jVectorSearchError
import logging
from dataclasses import dataclass

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="SGU Vector Search",
    page_icon="🔍",
    layout="wide"
)

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

def generate_answer(neo4j: Neo4jConnection, query: str, search_results: List[Dict]) -> Optional[str]:
    """Generate answer using OpenAI based on search results"""
    try:
        return neo4j.generate_answer(query, search_results)
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        st.error(f"Error generating answer: {str(e)}")
        return None
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
            answer = generate_answer(neo4j, userQuery, search_results)
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

 
# ─── main.py (phần quan trọng) ─────────────────────────────────────────────
def main() -> None:
    st.title("SGU Vector Search 🔍")

    # 1) Chọn client
    clients = init_neo4j_clients()
    client_name = st.sidebar.selectbox("🔧 Chọn mô hình", list(clients))
    neo4j_cfg = clients[client_name]
    neo4j = neo4j_cfg["conn"]
    labels = load_labels(neo4j_cfg["label_file"])     # ⚠ tất cả label hiện có

    # 2) Nhập truy vấn + tham số
    q = st.text_input("Nhập câu hỏi của bạn")
    col1, col2 = st.columns(2)
    with col1:
        min_sim = st.slider("Độ tương đồng tối thiểu", 0.0, 1.0, 0.5, 0.05)
    with col2:
        limit = st.slider("Kết quả tối đa / label", 1, 20, 10)

    # 3) Luôn tìm trên toàn bộ label
    node_types = labels                            # ← không còn chọn lọc

    # 4) Thực thi tìm kiếm
    if q.strip():
        with st.spinner("Đang tìm kiếm..."):
            results = perform_search(neo4j, q, node_types, min_sim, limit)

        if not results:
            st.warning("Không tìm thấy kết quả.")
            return

        with st.spinner("Đang tạo câu trả lời..."):
            answer = neo4j.generate_answer(q, results)

        st.subheader("📝 Câu trả lời")
        st.write(answer or "Không sinh được câu trả lời.")

        with st.expander("🔎 Chi tiết kết quả"):
            for r in results:
                st.markdown(
                    f"**{r['name']}** ({r['node_type']}) — "
                    f"Similarity: `{r['similarity']:.4f}`"
                )
                if desc := r.get("description"):
                    st.write(desc)
                st.divider()

if __name__ == "__main__":
    main()