from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS

# Fix the issue with incorrect use of literal
def process_ttl_file_fixed(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    header_lines = []
    class_lines = []
    in_class_section = False

    for line in lines:
        if line.strip().startswith("# Classes"):
            in_class_section = True
            continue
        if not in_class_section:
            header_lines.append(line)
        else:
            class_lines.append(line.strip())

    g = Graph()
    g.parse(data=''.join(header_lines), format='turtle')

    for prefix, ns in g.namespaces():
        if prefix == "":
            base_ns = Namespace(ns)
            break

    for line in class_lines:
        if not line or line.startswith('#'):
            continue
        parts = line.split(' a ')[0].strip(':')
        label = parts.strip()
        clean_name = normalize_label(label)  # Ensure normalize_label is defined below
        class_uri = URIRef(base_ns + clean_name)
        g.add((class_uri, RDF.type, RDFS.Class))
        g.add((class_uri, RDFS.label, Literal(label, lang='vi')))

    return g

# Define the normalize_label function
def normalize_label(label):
    # Replace spaces with underscores and convert to lowercase
    return label.replace(" ", "_").lower()

# Define new_graph_paths with appropriate mappings
new_graph_paths = {
    "deepseek_v3_0324": "../ontology/ontology_deepseek.ttl",
    "gemini_flash_thinking": "../ontology/ontology_openai.ttl",
    "openai_4o_mini": "../ontology/sgugemini.ttl",
}

# Reprocess the files correctly
fixed_output_paths = {}
for name, path in new_graph_paths.items():
    cleaned_graph = process_ttl_file_fixed(path)
    output_path = f"../ontology/cleaned_{name}.ttl"
    cleaned_graph.serialize(destination=output_path, format='turtle')
    fixed_output_paths[name] = output_path

