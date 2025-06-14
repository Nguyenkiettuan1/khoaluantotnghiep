"""
Configuration file for Evaluation Pipeline
==========================================

Chứa các tham số cấu hình cho pipeline evaluation
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Neo4j Configuration
NEO4J_CONFIG = {
    'uri': os.getenv('NEO4J_URI', 'bolt://localhost:7687'),
    'user': os.getenv('NEO4J_USER', 'neo4j'),
    'password': os.getenv('NEO4J_PASSWORD', 'password'),
    'databases': ['deepseek', 'gemini', 'openai']
}

# OpenAI Configuration
OPENAI_CONFIG = {
    'api_key': os.getenv('OPENAI_API_KEY'),
    'model': 'gpt-4o-mini',
    'temperature': 0,
    'max_tokens': 200
}

# Evaluation Parameters
EVALUATION_CONFIG = {
    'similarity_threshold': 0.6,
    'search_limit': 30,
    'score_threshold': 6,  # Điểm từ 6 trở lên được coi là "Right"
    'partial_threshold': 3  # Điểm dưới 3 được coi là "Wrong"
}

# File Paths
FILE_PATHS = {
    'golden_answers': 'sgu_golden_answers_updated.csv',
    'labels_dir': 'labels',
    'output_dir': 'evaluation_results',
    'charts_dir': 'evaluation_charts',
    'logs_dir': 'logs'
}

# Labels Files
LABELS_FILES = {
    'deepseek': 'labels/neo4j_labels_deepseek.txt',
    'gemini': 'labels/neo4j_labels_gemini.txt',
    'openai': 'labels/neo4j_labels_openai.txt'
}

# Output Files
OUTPUT_FILES = {
    'graph_analysis': 'graph_analysis_from_neo4j.csv',
    'answers': 'evaluation_answers_only.xlsx',
    'concepts': 'evaluation_kg_concepts.xlsx',
    'labels': 'evaluation_labels_only.xlsx',
    'concept_results': 'evaluation_concepts_result.xlsx',
    'summary_report': 'evaluation_summary_report.md'
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'file_prefix': 'evaluation_pipeline'
}
