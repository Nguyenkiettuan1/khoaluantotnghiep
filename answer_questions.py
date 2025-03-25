import os
import json
import openai
import numpy as np
from typing import List, Dict, Tuple
from neo4j import GraphDatabase
from urllib.parse import quote
from utils import load_txt_files, save_json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class RAGQuestionAnswerer:
    def __init__(self):
        """Initialize the RAG system with OpenAI and Neo4j connections"""
        # Get credentials from environment
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.neo4j_uri = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.neo4j_user = os.getenv('NEO4J_USER', 'neo4j')
        self.neo4j_password = os.getenv('NEO4J_PASSWORD')
        
        if not all([self.api_key, self.neo4j_password]):
            raise ValueError("Missing required environment variables")
            
        openai.api_key = self.api_key
        self.neo4j_driver = GraphDatabase.driver(
            self.neo4j_uri, 
            auth=(self.neo4j_user, self.neo4j_password)
        )
        
        self.documents = self.load_documents()
        self.document_embeddings = {}
        
    def load_documents(self) -> List[Dict]:
        """Load all PHẦN 1 documents and split into chunks"""
        documents = []
        
        # Get all files with prefix "PHẦN 1" from dataset directory
        files = load_txt_files("dataset", prefix="PHẦN 1")
        
        for file_info in files:
            # Split content into smaller chunks
            chunks = self.split_into_chunks(file_info['content'])
            for i, chunk in enumerate(chunks):
                documents.append({
                    'id': f"{file_info['filename']}_{i}",
                    'content': chunk,
                    'source': file_info['filename']
                })
        
        return documents
    
    def split_into_chunks(self, text: str, chunk_size: int = 1000) -> List[str]:
        """Split text into chunks of approximately chunk_size characters"""
        chunks = []
        words = text.split()
        current_chunk = []
        current_size = 0
        
        for word in words:
            word_size = len(word) + 1  # +1 for space
            if current_size + word_size > chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_size = word_size
            else:
                current_chunk.append(word)
                current_size += word_size
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using OpenAI"""
        try:
            response = openai.embeddings.create(
                model="text-embedding-3-small",
                input=text.replace("\n", " ")
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {str(e)}")
            return np.zeros(1536)  # Default embedding size for ada-002
    
    def compute_document_embeddings(self):
        """Compute embeddings for all documents"""
        for doc in self.documents:
            if doc['id'] not in self.document_embeddings:
                self.document_embeddings[doc['id']] = self.get_embedding(doc['content'])
    
    def find_relevant_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """Find most relevant documents for the query using embeddings"""
        query_embedding = self.get_embedding(query)
        
        # Ensure all documents have embeddings
        self.compute_document_embeddings()
        
        # Compute similarities
        similarities = {}
        for doc_id, doc_embedding in self.document_embeddings.items():
            similarity = np.dot(query_embedding, doc_embedding)
            similarities[doc_id] = similarity
        
        # Get top-k documents
        top_docs = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [next(doc for doc in self.documents if doc['id'] == doc_id) 
                for doc_id, _ in top_docs]
    
    def generate_answer(self, question: str, context_docs: List[Dict]) -> str:
        """Generate answer using GPT with retrieved context"""
        context = "\n\n".join([doc['content'] for doc in context_docs])
        
        prompt = f"""
        Answer the following question about Saigon University based on the provided context.
        If the answer cannot be fully determined from the context, say so.
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:
        """
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable assistant helping to answer questions about Saigon University."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating answer: {str(e)}")
            return "Error generating answer"
    
    def extract_entities_relations(self, question: str, answer: str) -> Dict:
        """Extract entities and relations from question-answer pair using GPT"""
        prompt = f"""
        Extract key entities and their relationships from this question and answer about Saigon University.
        Format as a valid JSON object with this exact structure:
        {{
            "entities": [
                {{"type": "entity_type", "id": "unique_id", "properties": {{"key": "value"}}}}
            ],
            "relations": [
                {{"source": "source_id", "type": "relation_type", "target": "target_id"}}
            ]
        }}
        
        Use only alphanumeric characters and underscores for IDs.

        Question: {question}
        Answer: {answer}
        """
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a knowledge graph expert. Output only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Extract and parse JSON
            content = response.choices[0].message.content.strip()
            try:
                start_idx = content.index('{')
                end_idx = content.rindex('}') + 1
                content = content[start_idx:end_idx]
                return json.loads(content)
            except (ValueError, json.JSONDecodeError) as e:
                print(f"Error parsing extracted information: {str(e)}")
                return {"entities": [], "relations": []}
                
        except Exception as e:
            print(f"Error extracting entities and relations: {str(e)}")
            return {"entities": [], "relations": []}
    
    def update_knowledge_graph(self, extracted_info: Dict):
        """Update Neo4j knowledge graph with extracted information"""
        with self.neo4j_driver.session() as session:
            # Create entities
            for entity in extracted_info['entities']:
                properties = {
                    k: v for k, v in entity['properties'].items()
                    if isinstance(v, (str, int, float, bool))
                }
                query = (
                    f"MERGE (n:{entity['type']} {{id: $id}}) "
                    "SET n += $properties"
                )
                session.run(query, id=entity['id'], properties=properties)
            
            # Create relations
            for relation in extracted_info['relations']:
                query = (
                    f"MATCH (a {{id: $source_id}}), (b {{id: $target_id}}) "
                    f"MERGE (a)-[r:{relation['type']}]->(b)"
                )
                session.run(
                    query,
                    source_id=relation['source'],
                    target_id=relation['target']
                )
    
    def process_questions(self, questions_file: str) -> List[Dict]:
        """Process all competency questions and update knowledge graph"""
        # Load questions
        with open(questions_file, 'r', encoding='utf-8') as f:
            questions = [line.strip() for line in f if line.strip()]
        
        results = []
        for i, question in enumerate(questions, 1):
            print(f"Processing question {i}/{len(questions)}")
            try:
                # Find relevant context
                relevant_docs = self.find_relevant_documents(question)
                
                # Generate answer
                answer = self.generate_answer(question, relevant_docs)
                
                # Extract entities and relations
                extracted_info = self.extract_entities_relations(question, answer)
                
                # Update knowledge graph
                self.update_knowledge_graph(extracted_info)
                
                results.append({
                    'question': question,
                    'answer': answer,
                    'extracted_info': extracted_info
                })
                
            except Exception as e:
                print(f"Error processing question: {str(e)}")
                results.append({
                    'question': question,
                    'error': str(e)
                })
        
        return results

def main():
    try:
        # Initialize RAG system
        rag = RAGQuestionAnswerer()
        
        # Process questions
        results = rag.process_questions("ontology/competency_questions.txt")
        
        # Save results
        output_file = "QA/qa_results.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        save_json(results, output_file)
        
        print(f"Processed {len(results)} questions")
        print(f"Results saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()