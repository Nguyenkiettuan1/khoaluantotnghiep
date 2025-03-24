import streamlit as st
import os
from dotenv import load_dotenv
from neo4jconnector import Neo4jConnection, Neo4jVectorSearchError
import logging

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

def perform_search(neo4j, query, node_types, min_similarity=0.5, limit=5):
    """Perform vector search across selected node types"""
    all_results = []
    
    for node_type in node_types:
        try:
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
            logger.error(f"Error searching {node_type}: {str(e)}")
            st.warning(f"Error searching {node_type}: {str(e)}")
            continue
    
    # Sort combined results by similarity
    return sorted(all_results, key=lambda x: x['similarity'], reverse=True)

def generate_answer(neo4j, query, search_results):
    """Generate answer using OpenAI based on search results"""
    try:
        answer = neo4j.generate_answer(query, search_results)
        return answer
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        st.error(f"Error generating answer: {str(e)}")
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
    
    # Node type selection
    node_types = st.multiselect(
        "Chọn loại nội dung tìm kiếm",
        ["Department", "TrainingProgram", "InternationalCooperation", 
         "Scholarship", "ResearchTopic", "Journal"],
        default=["Department", "TrainingProgram"]
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