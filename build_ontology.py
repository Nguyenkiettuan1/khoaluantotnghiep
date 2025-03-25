import os
import json
from urllib.parse import quote
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL, XSD
import openai
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class UniversityOntologyBuilder:
    def __init__(self, api_key: str = None):
        self.g = Graph()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not provided or found in environment")
        openai.api_key = self.api_key
        
        # Define namespaces
        self.uni = Namespace("http://www.saigonuni.edu.vn/ontology#")
        self.g.bind("uni", self.uni)
    
    def _safe_uri(self, name: str) -> URIRef:
        """Create a safe URI by encoding spaces and special characters"""
        # Remove special characters and replace spaces with underscores
        safe_name = name.replace(" ", "_").replace("(", "").replace(")", "")
        safe_name = "".join(c for c in safe_name if c.isalnum() or c in "_-")
        return self.uni[safe_name]
    
    def load_concepts_analysis(self, file_path: str) -> Dict:
        """Load concepts and relationships analysis from file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def create_ontology_from_concepts(self, concepts_analysis: Dict):
        """Create ontology classes and properties from concepts analysis"""
        # Create classes from concepts
        for concept in concepts_analysis['concepts']:
            class_uri = self._safe_uri(concept['name'])
            self.g.add((class_uri, RDF.type, OWL.Class))
            self.g.add((class_uri, RDFS.label, Literal(concept['name'], lang="en")))
            self.g.add((class_uri, RDFS.comment, Literal(concept['description'], lang="en")))
            
            # Add datatype properties
            for prop in concept['properties']:
                prop_uri = self._safe_uri(f"has_{prop}")
                self.g.add((prop_uri, RDF.type, OWL.DatatypeProperty))
                self.g.add((prop_uri, RDFS.domain, class_uri))
                # Infer property range based on common patterns
                if any(x in prop.lower() for x in ['date', 'time', 'year']):
                    self.g.add((prop_uri, RDFS.range, XSD.dateTime))
                elif any(x in prop.lower() for x in ['number', 'count', 'amount']):
                    self.g.add((prop_uri, RDFS.range, XSD.integer))
                else:
                    self.g.add((prop_uri, RDFS.range, XSD.string))
        
        # Create object properties from relationships
        for rel in concepts_analysis['relationships']:
            source_uri = self._safe_uri(rel['source'])
            target_uri = self._safe_uri(rel['target'])
            rel_uri = self._safe_uri(rel['type'])
            
            self.g.add((rel_uri, RDF.type, OWL.ObjectProperty))
            self.g.add((rel_uri, RDFS.domain, source_uri))
            self.g.add((rel_uri, RDFS.range, target_uri))
    
    def enrich_ontology_with_gpt(self):
        """Use GPT to suggest additional ontology enrichments"""
        # Convert current ontology to string format for GPT
        ontology_str = self.g.serialize(format='turtle').decode('utf-8') if isinstance(self.g.serialize(format='turtle'), bytes) else self.g.serialize(format='turtle')
        
        prompt = f"""
        Analyze this ontology and suggest additional:
        1. Classes that might be missing
        2. Properties for existing classes
        3. Relationships between classes
        4. Axioms or restrictions
        
        Format your response as JSON with this exact structure:
        {{
            "new_classes": [
                {{"name": "class_name", "description": "class_description", "properties": ["prop1", "prop2"]}}
            ],
            "new_relationships": [
                {{"source": "source_class", "target": "target_class", "type": "relationship_type"}}
            ]
        }}
        
        Current ontology:
        {ontology_str}
        """
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an ontology engineering expert. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Extract and parse JSON from response
            content = response.choices[0].message.content.strip()
            try:
                start_idx = content.index('{')
                end_idx = content.rindex('}') + 1
                content = content[start_idx:end_idx]
                suggestions = json.loads(content)
            except (ValueError, json.JSONDecodeError) as e:
                print(f"Error parsing GPT suggestions: {str(e)}")
                return
            
            # Apply suggestions
            for class_info in suggestions.get('new_classes', []):
                class_uri = self._safe_uri(class_info['name'])
                self.g.add((class_uri, RDF.type, OWL.Class))
                self.g.add((class_uri, RDFS.label, Literal(class_info['name'], lang="en")))
                if 'description' in class_info:
                    self.g.add((class_uri, RDFS.comment, Literal(class_info['description'], lang="en")))
                
                for prop in class_info.get('properties', []):
                    prop_uri = self._safe_uri(f"has_{prop}")
                    self.g.add((prop_uri, RDF.type, OWL.DatatypeProperty))
                    self.g.add((prop_uri, RDFS.domain, class_uri))
            
            for rel in suggestions.get('new_relationships', []):
                source_uri = self._safe_uri(rel['source'])
                target_uri = self._safe_uri(rel['target'])
                rel_uri = self._safe_uri(rel['type'])
                
                self.g.add((rel_uri, RDF.type, OWL.ObjectProperty))
                self.g.add((rel_uri, RDFS.domain, source_uri))
                self.g.add((rel_uri, RDFS.range, target_uri))
                
        except Exception as e:
            print(f"Error enriching ontology: {str(e)}")
    
    def generate_neo4j_mapping(self) -> str:
        """Generate Cypher queries for Neo4j schema based on ontology"""
        cypher_queries = []
        
        # Create node label constraints
        for s, p, o in self.g.triples((None, RDF.type, OWL.Class)):
            class_name = str(s).split('#')[-1]
            cypher_queries.append(f"CREATE CONSTRAINT IF NOT EXISTS FOR (n:{class_name}) REQUIRE n.uri IS UNIQUE;")
        
        # Create relationship types
        for s, p, o in self.g.triples((None, RDF.type, OWL.ObjectProperty)):
            rel_name = str(s).split('#')[-1]
            domain = next(self.g.objects(s, RDFS.domain)).split('#')[-1]
            range_class = next(self.g.objects(s, RDFS.range)).split('#')[-1]
            cypher_queries.append(
                f"MATCH (a:{domain}), (b:{range_class}) "
                f"WHERE a.uri = $a_uri AND b.uri = $b_uri "
                f"CREATE (a)-[r:{rel_name}]->(b);"
            )
        
        return "\n".join(cypher_queries)
    
    def save_ontology(self, file_path: str):
        """Save the ontology to a file"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.g.serialize(destination=file_path, format="turtle")
    
    def save_neo4j_mapping(self, file_path: str):
        """Save Neo4j mapping queries to a file"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        mapping = self.generate_neo4j_mapping()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(mapping)

def main():
    try:
        # Get OpenAI API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        # Initialize builder
        builder = UniversityOntologyBuilder(api_key)
        
        # Load concepts analysis
        concepts_analysis = builder.load_concepts_analysis("ontology/concepts_analysis.json")
        
        # Create initial ontology
        builder.create_ontology_from_concepts(concepts_analysis)
        
        # Enrich ontology using GPT
        builder.enrich_ontology_with_gpt()
        
        # Save ontology
        builder.save_ontology("ontology/ontology_generated.ttl")
        
        # Save Neo4j mapping
        builder.save_neo4j_mapping("cypher/populate_ontology.cypher")
        
        print("Ontology and Neo4j mapping generated successfully")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()