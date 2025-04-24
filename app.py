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

def init_neo4j():
    """Initialize Neo4j connection"""
    try:
        return Neo4jConnection(
            uri=os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
            user=os.getenv('NEO4J_USER', 'neo4j'),
            password=os.getenv('NEO4J_PASSWORD'),
            dbname=os.getenv('NEO4J_DATABASE', 'neo4j')
        )
    except Exception as e:
        st.error(f"Failed to connect to Neo4j: {str(e)}")
        return None

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
        search_results = perform_search(neo4j, userQuery, labels, min_similarity=0.6, limit=10)
        
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



def main():
    st.title("SGU Vector Search 🔍")
    
    # Initialize Neo4j connection
    neo4j = init_neo4j()
    if not neo4j:
        st.stop()
    
    # Main search interface
    st.header("Tìm kiếm thông tin")
    
    # Search parameters
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_query = st.text_input("Nhập câu hỏi của bạn")
    with col2:
        min_similarity = st.slider("Độ tương đồng tối thiểu", 0.0, 1.0, 0.5, 0.1)
    with col3:
        max_results = st.slider("Số kết quả tối đa mỗi loại", 1, 10, 5)

    # Load and process node type labels
    with open("labels/neo4j_labels_deepseek.txt", "r") as f:
        type_labels = [label.strip() for label in f.read().splitlines() if label.strip()]
    
    # Node type selection
    default_types = ["Department"]  # Default selection that we know exists
    default_types = [t for t in default_types if t in type_labels]  # Validate defaults
    
    node_types = st.multiselect(
        "Chọn loại nội dung tìm kiếm",
        type_labels,
        default=default_types
    )
    
    # Perform search
    if search_query and node_types:
        with st.spinner('Đang tìm kiếm...'):
            try:
                # Get search results
                results = perform_search(
                    neo4j, 
                    search_query, 
                    node_types, 
                    min_similarity, 
                    max_results
                )
                
                if results:
                    # Generate answer
                    with st.spinner('Đang tạo câu trả lời...'):
                        answer = generate_answer(neo4j, search_query, results)
                        
                        if answer:
                            st.header("Câu trả lời")
                            st.write(answer)
                            
                            # Show search results in an expander
                            with st.expander("Xem kết quả tìm kiếm chi tiết"):
                                for result in results:
                                    st.markdown(
                                        f"**{result['name']}** ({result['node_type']}) - "
                                        f"Độ tương đồng: {result['similarity']:.4f}"
                                    )
                                    if result.get('description'):
                                        st.markdown(f"*{result['description']}*")
                                    st.markdown("---")
                else:
                    st.info("Không tìm thấy kết quả phù hợp với tiêu chí của bạn")
                    
            except Exception as e:
                logger.error(f"Search error: {str(e)}")
                st.error(f"Đã xảy ra lỗi trong quá trình tìm kiếm: {str(e)}")

if __name__ == "__main__":
    main()