import os

from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")
dbname = os.getenv("NEO4J_DATABASE")
print(uri, neo4j_user, neo4j_password, dbname)