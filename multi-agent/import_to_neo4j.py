import os
from neo4jconnector import Neo4jConnection
from typing import List
import logging
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelDatabase:
    def __init__(self, name: str, cypher_dir: str, db_name: str):
        """
        Initialize model database configuration
        Args:
            name: Name of the model (DeepSeek, Gemini, OpenAI)
            cypher_dir: Directory containing Cypher files
            db_name: Neo4j database name
        """
        self.name = name
        self.cypher_dir = cypher_dir
        self.db_name = db_name
        self.connection = None

    def connect(self):
        """Connect to Neo4j database"""
        try:
            self.connection = Neo4jConnection(
                uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
                user=os.getenv("NEO4J_USER", "neo4j"),
                password=os.getenv("NEO4J_PASSWORD", "password"),
                dbname=self.db_name
            )
            logger.info(f"Connected to database {self.db_name} for {self.name}")
        except Exception as e:
            logger.error(f"Failed to connect to database {self.db_name}: {str(e)}")
            raise

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info(f"Closed connection to database {self.db_name}")

def read_cypher_files(directory: str) -> List[tuple]:
    """
    Read all Cypher files from a directory in sorted order
    Returns list of tuples (filename, content)
    """
    cypher_files = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".cypher"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                cypher_files.append((filename, content))
    return cypher_files

def execute_cypher(db: ModelDatabase, cypher_content: str, filename: str):
    """Execute Cypher content from file"""
    try:
        # Execute entire file content as one transaction
        db.connection.run_cypher(cypher_content)
        logger.info(f"Successfully executed queries from {filename}")
    except Exception as e:
        logger.error(f"Error executing {filename}: {str(e)}")
        raise

def main():
    # Define model databases
    models = [
        ModelDatabase("DeepSeek", "./cypher_deepseek_sguv1", "deepseek_kg"),
        ModelDatabase("Gemini", "./cypher_gemini_sguv2", "gemini_kg"),
        ModelDatabase("OpenAI", "./cypher_openai_sguv3", "openai_kg")
    ]

    for model_db in models:
        try:
            logger.info(f"\n=== Processing {model_db.name} model ===")
            
            # Connect to database
            model_db.connect()
            
            # Read and execute Cypher files
            cypher_files = read_cypher_files(model_db.cypher_dir)
            logger.info(f"Found {len(cypher_files)} Cypher files for {model_db.name}")
            
            for filename, content in cypher_files:
                logger.info(f"Processing {filename}")
                execute_cypher(model_db, content, filename)
                
        except Exception as e:
            logger.error(f"Error processing {model_db.name}: {str(e)}")
            continue
            
        finally:
            # Always close connection
            model_db.close()

    logger.info("\nFinished importing data to Neo4j databases")

if __name__ == "__main__":
    main()