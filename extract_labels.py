from neo4jconnector import Neo4jConnection
import os
from dotenv import load_dotenv

def extract_labels_to_file(output_file: str = "labels/neo4j_labels.txt"):
    """
    Extract all labels from Neo4j database and save to file
    
    Args:
        output_file: Path to output file
    """
    # Load environment variables
    load_dotenv()
    
    # Create labels directory if not exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Connect to Neo4j
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")
    # database = os.getenv("NEO4J_DATABASE", "neo4j")
    database = "openai"
    
    # Initialize connection
    neo4j_connection = Neo4jConnection(uri, user, password, database)
    
    try:
        # Get all labels using Cypher query
        query = "CALL db.labels()"
        results = neo4j_connection.run_cypher(query)
        
        # Extract labels from results
        labels = sorted([result["label"] for result in results])
        
        # Write labels to file
        with open(output_file, "w", encoding="utf-8") as f:
            for label in labels:
                f.write(f"{label}\n")
        
        print(f"Successfully extracted {len(labels)} name to {output_file}")
        
    finally:
        # Close connection
        neo4j_connection.close()

if __name__ == "__main__":
    extract_labels_to_file('labels/neo4j_labels_openai.txt')