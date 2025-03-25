import os
from typing import List
import openai
import json
from utils import load_txt_files, save_text, save_json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class CompetencyQuestionGenerator:
    def __init__(self):
        # Get OpenAI API key from environment variables
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        openai.api_key = self.api_key
        
    def collect_phan1_data(self) -> str:
        """Collect all text data from PHẦN 1 sections"""
        documents = load_txt_files("dataset", prefix="PHẦN 1")
        all_content = "\n\n".join([doc['content'] for doc in documents])
        return all_content

    def generate_competency_questions(self, text_data: str) -> List[str]:
        """Generate competency questions using OpenAI"""
        prompt = f"""
        Based on the following text about Saigon University, generate competency questions that will help build an ontology.
        Focus on creating questions that cover:
        1. Organization structure (departments, faculties, units)
        2. Education programs (bachelor, master, PhD)
        3. International cooperation (partnerships, exchange programs)
        4. Research activities (student research, publications)
        5. Infrastructure (campuses, facilities)
        
        Format each question as CQ<number>: <question>
        Generate at least 3 questions for each category.
        
        Text:
        {text_data}
        """
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a knowledge engineer helping to build a university ontology."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract questions from response
            questions_text = response.choices[0].message.content
            questions = [line.strip() for line in questions_text.split('\n') if line.strip().startswith('CQ')]
            
            return questions
        except Exception as e:
            print(f"Error generating questions: {str(e)}")
            return []

    def analyze_concepts(self, questions: List[str]) -> dict:
        """Analyze concepts and relationships from competency questions using OpenAI"""
        prompt = f"""
        Analyze these competency questions and identify key concepts and relationships for building a university ontology.
        Return only a valid JSON object with the following exact structure:
        {{
            "concepts": [
                {{"name": "concept_name", "description": "concept_description", "properties": ["prop1", "prop2"]}},
                ...
            ],
            "relationships": [
                {{"source": "concept1", "target": "concept2", "type": "relationship_type"}},
                ...
            ]
        }}

        Ensure that:
        1. All JSON keys and values are properly quoted
        2. Arrays and objects are properly terminated
        3. No trailing commas in arrays or objects

        Competency Questions to analyze:
        {json.dumps(questions, ensure_ascii=False, indent=2)}
        """
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are a knowledge engineer that outputs only valid JSON. 
                        Your responses must be properly formatted JSON objects that can be parsed by json.loads()."""
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Get response content
            content = response.choices[0].message.content.strip()
            
            # Try to find JSON object if there's any surrounding text
            try:
                start_idx = content.index('{')
                end_idx = content.rindex('}') + 1
                content = content[start_idx:end_idx]
            except ValueError:
                raise ValueError("No valid JSON object found in response")
            
            # Parse JSON
            try:
                concepts_analysis = json.loads(content)
            except json.JSONDecodeError as e:
                print(f"Invalid JSON response: {content}")
                raise ValueError(f"Failed to parse JSON response: {str(e)}")
            
            # Validate structure
            if not isinstance(concepts_analysis, dict):
                raise ValueError("Response is not a JSON object")
            if "concepts" not in concepts_analysis or "relationships" not in concepts_analysis:
                raise ValueError("Response missing required keys: concepts, relationships")
            
            return concepts_analysis
            
        except Exception as e:
            print(f"Error analyzing concepts: {str(e)}")
            # Return a minimal valid structure
            return {
                "concepts": [
                    {
                        "name": "University",
                        "description": "Educational institution",
                        "properties": ["name", "location"]
                    }
                ],
                "relationships": []
            }

def main():
    try:
        # Initialize generator
        generator = CompetencyQuestionGenerator()
        
        # Create necessary directories
        os.makedirs("ontology", exist_ok=True)
        
        # Collect data
        print("Collecting data from PHẦN 1 sections...")
        university_data = generator.collect_phan1_data()
        
        # Generate questions
        print("Generating competency questions...")
        questions = generator.generate_competency_questions(university_data)
        
        if not questions:
            raise ValueError("No questions were generated")
        
        # Save questions
        output_file = "ontology/competency_questions.txt"
        save_text('\n'.join(questions), output_file)
        
        # Analyze concepts and relationships
        print("Analyzing concepts and relationships...")
        concepts_analysis = generator.analyze_concepts(questions)
        
        # Save concepts analysis
        concepts_file = "ontology/concepts_analysis.json"
        save_json(concepts_analysis, concepts_file)
        
        print(f"Generated {len(questions)} competency questions")
        print(f"Questions saved to: {output_file}")
        print(f"Concepts analysis saved to: {concepts_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()