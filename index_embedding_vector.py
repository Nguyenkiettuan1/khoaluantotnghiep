from neo4jconnector import Neo4jConnection
from dotenv import load_dotenv
import os
import logging 
def create_vector_indexes(neo4j : Neo4jConnection):
    """Create vector indexes for all node types"""

    with open("labels/neo4j_labels_openai.txt", "r") as f:
        node_labels = f.read().splitlines()
    
    print("Creating vector indexes...")
    for label in node_labels:
        try:
            index_name = f"{label.lower()}_embedding_index"
            neo4j.create_vector_index(
                index_name=index_name,
                node_label=label
            )
            print(f"Created index: {index_name}")
        except Exception as e:
            print(f"Error creating index for {label}: {str(e)}")

def add_embeddings_to_all_nodes(neo4j):
    """Add embeddings to all nodes in the database"""
    try:
        # Get all nodes that don't have an embedding yet
        query = """
        MATCH (n)
        WHERE n.name IS NOT NULL 
        AND n.embedding IS NULL
        RETURN DISTINCT labels(n) as labels, n.name as name, ID(n) as id
        """
        nodes = neo4j.run_cypher(query)
        
        if not nodes:
            print("All nodes already have embeddings")
            return
            
        print(f"\nAdding embeddings to nodes...")
        
        for node in nodes:
            try:
                # Get additional text properties for richer embedding context
                properties_query = """
                MATCH (n)
                WHERE ID(n) = $node_id
                RETURN properties(n) as props
                """
                props = neo4j.run_cypher(properties_query, {"node_id": node['id']})[0]['props']
                
                # Combine relevant text properties for embedding
                text_props = []
                for key, value in props.items():
                    if isinstance(value, str) and key != 'name' and 'embedding' not in key.lower():
                        text_props.append(f"{key}: {value}")
                
                # Generate embedding based on node name and properties
                node_text = node['name']
                if text_props:
                    node_text = f"{node_text}. {'. '.join(text_props)}"
                
                # Generate and store embedding
                embedding = neo4j.generate_embedding(node_text)
                
                # Update node with embedding
                labels_str = ':'.join(node['labels'])
                update_query = f"""
                MATCH (n:{labels_str}) WHERE ID(n) = $node_id
                SET n.embedding = $embedding
                """
                neo4j.run_cypher(update_query, {
                    "node_id": node['id'],
                    "embedding": embedding
                })
                print(f"Added embedding to {labels_str} node: {node['name']}")
                
            except Exception as e:
                print(f"Error processing node {node['name']}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Error in add_embeddings_to_all_nodes: {str(e)}")
        raise


def main():
    # Load environment variables
    load_dotenv()
    
    try:
        # Initialize Neo4j connection
        neo4j = Neo4jConnection(
            uri=os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
            user=os.getenv('NEO4J_USER', 'neo4j'),
            password=os.getenv('NEO4J_PASSWORD'),
            # dbname=os.getenv('NEO4J_DATABASE', 'neo4j')
            dbname="openai"
        )
        
        try:
            # Step 1: Create vector indexes for all node types
            create_vector_indexes(neo4j)
            
            # Step 2: Add embeddings to all nodes
            add_embeddings_to_all_nodes(neo4j)
          
            
        except Exception as e:
            print(f"Error during execution: {str(e)}")
        finally:
            neo4j.close()
            
    except Exception as e:
        print(f"Error initializing Neo4j connection: {str(e)}")

if __name__ == "__main__":
    main()