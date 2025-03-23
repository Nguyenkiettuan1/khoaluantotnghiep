import os

from utils import run_test_queries_and_save_results


uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")
dbname = os.getenv("NEO4J_DATABASE")

run_test_queries_and_save_results(
    uri=uri,
    user=neo4j_user,
    password=neo4j_password,
    dbname=dbname
)