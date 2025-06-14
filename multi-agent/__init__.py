"""
Multi-Agent Ontology Generation System

Hệ thống tạo ontology tự động sử dụng nhiều mô hình AI để xây dựng knowledge graph từ dữ liệu văn bản.

Main modules:
- main: Workflow orchestrator
- generate_cqs: Generate competency questions
- generate_skeleton_ontology: Create basic ontology structure  
- generate_ontology_parallel: Multi-agent Cypher generation
- import_to_neo4j: Neo4j database import
- neo4jconnector: Neo4j connection and vector search
- model_configs: AI model configurations
"""

__version__ = "1.0.0"
__author__ = "SGU Ontology Team"

# Import main components
from .main import OntologyWorkflow
from .neo4jconnector import Neo4jConnection
from .model_configs import DeepSeekConfig, OpenAIConfig
from .gemini_config import GeminiConfig

__all__ = [
    'OntologyWorkflow',
    'Neo4jConnection', 
    'DeepSeekConfig',
    'OpenAIConfig',
    'GeminiConfig'
]
