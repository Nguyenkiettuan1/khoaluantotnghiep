import os
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase
from openai import OpenAI
import numpy as np
from dotenv import load_dotenv

# Configure logging with UTF-8 encoding
def setup_logger():
    """Configure logging to both file and console with UTF-8 encoding"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create a logger
    logger = logging.getLogger('neo4j_vector_search')
    logger.setLevel(logging.DEBUG)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )

    # File handler with UTF-8 encoding
    file_handler = logging.FileHandler(
        f'logs/neo4j_vector_search_{datetime.now().strftime("%Y%m%d")}.log',
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # Console handler with UTF-8 encoding
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Initialize logger
logger = setup_logger()

class Neo4jVectorSearchError(Exception):
    """Custom exception for Neo4j vector search operations"""
    pass

class Neo4jConnection:
    # OpenAI configuration
    EMBEDDING_MODEL = "text-embedding-ada-002"
    CHAT_MODEL = "gpt-4o-mini"
    EMBEDDING_DIMENSION = 1536

    def __init__(self, uri: str, user: str, password: str, dbname: str):
        """
        Initialize Neo4j connection with vector search capabilities
        
        Args:
            uri: Neo4j database URI
            user: Database username
            password: Database password
            dbname: Database name
        """
        try:
            logger.info(f"Initializing Neo4j connection to {uri}")
            self._driver = GraphDatabase.driver(uri, auth=(user, password), database=dbname)
            
            # Initialize OpenAI client
            load_dotenv()
            self._openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            logger.info("Successfully initialized Neo4j and OpenAI clients")
            
            # Test connection
            self.test_connection()
        except Exception as e:
            logger.error(f"Failed to initialize connection: {str(e)}")
            raise Neo4jVectorSearchError(f"Failed to initialize connection: {str(e)}")

    def test_connection(self):
        """Test the Neo4j connection"""
        try:
            with self._driver.session() as session:
                session.run("RETURN 1")
            logger.info("Neo4j connection test successful")
        except Exception as e:
            logger.error(f"Neo4j connection test failed: {str(e)}")
            raise Neo4jVectorSearchError(f"Connection test failed: {str(e)}")

    def close(self):
        """Close the Neo4j connection"""
        self._driver.close()
        logger.info("Neo4j connection closed")

    def run_cypher(self, cypher_query: str, parameters: dict = None) -> List[Dict]:
        """
        Execute a Cypher query
        
        Args:
            cypher_query: Cypher query string
            parameters: Optional query parameters
            
        Returns:
            List of query results
        """
        try:
            logger.debug(f"Executing Cypher query: {cypher_query}")
            logger.debug(f"Query parameters: {parameters}")
            
            with self._driver.session() as session:
                result = session.run(cypher_query, parameters or {})
                data = result.data()
                logger.debug(f"Query returned {len(data)} results")
                return data
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            raise Neo4jVectorSearchError(f"Query execution failed: {str(e)}")



    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using OpenAI
        
        Args:
            text: Input text
            
        Returns:
            List of embedding values
        """
        try:
            logger.debug(f"Generating embedding for text: {text[:100]}...")
            response = self._openai_client.embeddings.create(
                model=self.EMBEDDING_MODEL,
                input=text
            )
            logger.debug("Successfully generated embedding")
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            raise Neo4jVectorSearchError(f"Failed to generate embedding: {str(e)}")

    def similarity_search(self,
                        query_text: str,
                        node_label: str,
                        limit: int = 5,
                        min_similarity: float = 0.0,
                        embedding_property: str = "embedding") -> List[Dict]:
        """
        Perform similarity search
        
        Args:
            query_text: Search query text
            node_label: Label of nodes to search
            limit: Maximum number of results
            min_similarity: Minimum similarity threshold
            embedding_property: Name of the embedding property
            
        Returns:
            List of similar documents with their properties and similarity scores
        """
        try:
            logger.info(f"Performing similarity search for query: {query_text}")
            
            # Generate query embedding
            query_embedding = self.generate_embedding(query_text)
            
            # Perform similarity search
            search_query = f"""
            CALL {{
                WITH $embedding AS query
                MATCH (n:{node_label})
                WHERE n.{embedding_property} IS NOT NULL
                WITH n, gds.similarity.cosine(query, n.{embedding_property}) AS similarity
                WHERE similarity >= $min_similarity
                RETURN n, similarity
                ORDER BY similarity DESC
                LIMIT $limit
            }}
            RETURN n.name AS name, n.description as description, similarity
            """
            
            params = {
                "embedding": query_embedding,
                "min_similarity": min_similarity,
                "limit": limit
            }
            
            results = self.run_cypher(search_query, params)
            logger.info(f"Found {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Similarity search failed: {str(e)}")
            raise Neo4jVectorSearchError(f"Similarity search failed: {str(e)}")

    def generate_answer(self, query: str, search_results: List[Dict]) -> str:
        """
        Generate an answer using OpenAI based on search results
        
        Args:
            query: User's question
            search_results: List of search results with name and description
            
        Returns:
            Generated answer
        """
        try:
            # Format context from search results
            context = "\n\n".join([
                f"Thông tin {result['node_type']}:\n"
                f"Tên: {result['name']}\n"
                f"Mô tả: {result.get('description', 'Không có mô tả')}\n"
                f"Độ tương đồng: {result['similarity']:.4f}"
                for result in sorted(search_results, key=lambda x: x['similarity'], reverse=True)
            ])
            
            # Prepare the prompt
            messages = [
                {"role": "system", "content": """
                Bạn là trợ lý AI của trường Đại học Sài Gòn (SGU). Nhiệm vụ của bạn là trả lời câu hỏi dựa trên kết quả tìm kiếm được cung cấp.

                Hướng dẫn:
                1. Chỉ sử dụng thông tin từ kết quả tìm kiếm để trả lời
                2. Nếu thông tin trong kết quả tìm kiếm không đủ để trả lời câu hỏi, hãy nói rõ điều đó
                3. Nếu độ tương đồng của kết quả tìm kiếm cao (>0.6) và thông tin phù hợp với câu hỏi, hãy trả lời chi tiết
                4. Trình bày câu trả lời một cách rõ ràng, mạch lạc và chuyên nghiệp
                5. Nếu thấy thông tin mâu thuẫn giữa các kết quả, hãy nêu rõ điều này
                6. Nếu câu hỏi yêu cầu thông tin cụ thể (như số lượng, địa điểm, thời gian) mà không tìm thấy trong kết quả, hãy nói rõ là không có thông tin này
                7. Khi đề cập đến học bổng hoặc thông tin quan trọng, hãy cung cấp thông tin chi tiết từ kết quả tìm kiếm, không đưa ra giả định
                8. Hãy phân tích độ tin cậy của thông tin dựa trên độ tương đồng trước khi đưa ra câu trả lời

                Luôn bắt đầu câu trả lời bằng cách đánh giá mức độ tin cậy của thông tin dựa trên độ tương đồng và độ phù hợp với câu hỏi.
                """},
                {"role": "user", "content": f"""
                Câu hỏi: {query}
                
                Kết quả tìm kiếm:
                {context}
                
                Hãy trả lời câu hỏi dựa trên những kết quả tìm kiếm này.
                """}
            ]
            
            # Generate answer
            logger.info("Generating answer using OpenAI")
            response = self._openai_client.chat.completions.create(
                model=self.CHAT_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content.strip()
            logger.info("Successfully generated answer")
            return answer
            
        except Exception as e:
            logger.error(f"Failed to generate answer: {str(e)}")
            raise Neo4jVectorSearchError(f"Failed to generate answer: {str(e)}")
