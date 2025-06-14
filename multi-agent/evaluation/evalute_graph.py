
from matplotlib import pyplot as plt
import pandas as pd
import networkx as nx
import json
from neo4j import GraphDatabase

def build_and_visualize_graph_from_neo4j(name, neo4j_uri, neo4j_user, neo4j_password, database_name):
    """
    Đọc dữ liệu từ Neo4j và tạo graph
    """
    
    def get_nodes_and_edges_from_neo4j(uri, user, password, database):
        """Lấy nodes và edges từ Neo4j"""
        driver = GraphDatabase.driver(uri, auth=(user, password))
        nodes_data = []
        edges_data = []
        
        with driver.session(database=database) as session:
            # SỬA LỖI: Sử dụng elementId() thay vì id()
            nodes_query = """
            MATCH (n)
            RETURN elementId(n) as id, 
                   labels(n) as labels, 
                   properties(n) as properties
            """
            
            result = session.run(nodes_query)
            for record in result:
                nodes_data.append({
                    'id': record['id'],
                    'labels': record['labels'],
                    'properties': record['properties']
                })
            
            # SỬA LỖI: Sử dụng elementId() thay vì id()
            edges_query = """
            MATCH (a)-[r]->(b)
            RETURN elementId(a) as source, 
                   elementId(b) as target, 
                   type(r) as type,
                   properties(r) as properties
            """
            
            result = session.run(edges_query)
            for record in result:
                edges_data.append({
                    'source': record['source'],
                    'target': record['target'],
                    'type': record['type'],
                    'properties': record['properties']
                })
        
        driver.close()
        return nodes_data, edges_data
    
    try:
        print(f"📖 Loading {name} from Neo4j database: {database_name}")
        
        # Lấy dữ liệu từ Neo4j
        nodes_data, edges_data = get_nodes_and_edges_from_neo4j(
            neo4j_uri, neo4j_user, neo4j_password, database_name
        )
        
        print(f"   Nodes: {len(nodes_data)}, Edges: {len(edges_data)}")
        
        # Tạo NetworkX graph
        G = nx.DiGraph()
        
        # SỬA LỖI: Tách riêng properties để tránh conflict
        for node in nodes_data:
            node_id = str(node['id'])
            labels = node['labels'] if node['labels'] else []
            properties = node['properties'] if node['properties'] else {}
            
            # Tạo safe properties - tránh conflict với NetworkX parameters
            safe_props = {}
            node_name = "Unknown"
            node_description = ""
            
            # Extract name và description safely
            if properties:
                if 'name' in properties:
                    node_name = properties['name']
                elif 'title' in properties:
                    node_name = properties['title']
                elif 'label' in properties:
                    node_name = properties['label']
                else:
                    node_name = f"Node_{node_id}"
                
                if 'description' in properties:
                    node_description = properties['description']
                
                # Copy other properties (excluding ones that might conflict)
                for key, value in properties.items():
                    if key not in ['name', 'description']:
                        safe_props[key] = value
            
            # Add node with safe parameters
            G.add_node(node_id,
                      labels=labels,
                      node_name=node_name,  # Renamed from 'name' to avoid conflicts
                      node_description=node_description,  # Renamed from 'description'
                      **safe_props)
        
        # Thêm edges
        for edge in edges_data:
            source_id = str(edge['source'])
            target_id = str(edge['target'])
            edge_type = edge['type']
            properties = edge['properties'] if edge['properties'] else {}
            
            G.add_edge(source_id, target_id,
                      edge_type=edge_type,  # Renamed from 'type'
                      **properties)
        
        print(f"✅ Created graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        
        # Vẽ subgraph với top 20 nodes có degree cao nhất
        if G.number_of_nodes() > 0:
            visualize_top_nodes_subgraph(G, name, top_k=20)
        
        return G
        
    except Exception as e:
        print(f"❌ Error loading {name} from Neo4j: {e}")
        import traceback
        traceback.print_exc()
        return nx.DiGraph()  # Return empty graph


def visualize_top_nodes_subgraph(G, name, top_k=20):
    """Vẽ subgraph của top k nodes có degree cao nhất"""
    
    if G.number_of_nodes() == 0:
        print(f"⚠️ Empty graph for {name}")
        return
    
    try:
        # Tính degree centrality
        degree_centrality = nx.degree_centrality(G)
        
        # Lấy top k nodes
        top_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:top_k]
        top_node_ids = [n for n, _ in top_nodes]
        
        # Tạo subgraph
        H = G.subgraph(top_node_ids)
        
        if H.number_of_nodes() == 0:
            print(f"⚠️ No nodes to visualize for {name}")
            return
        
        # Vẽ graph
        plt.figure(figsize=(14, 10))
        pos = nx.spring_layout(H, seed=42, k=2, iterations=50)
        
        # SỬA LỖI: Sử dụng attribute names đã rename
        node_labels = {}
        for n in H.nodes():
            node_name = G.nodes[n].get("node_name", "")  # Changed from "name"
            if not node_name or node_name == f"Node_{n}":
                # Nếu không có name, thử lấy từ properties khác
                props = G.nodes[n]
                node_name = (props.get("title", "") or 
                           props.get("label", "") or 
                           f"Node_{n}")
            # Cắt ngắn tên nếu quá dài
            if len(node_name) > 15:
                node_name = node_name[:12] + "..."
            node_labels[n] = node_name
        
        # Vẽ nodes và edges
        nx.draw_networkx_nodes(H, pos, node_size=800, node_color="lightblue", 
                              alpha=0.7, edgecolors="black", linewidths=1)
        nx.draw_networkx_edges(H, pos, edge_color="gray", alpha=0.5, 
                              arrows=True, arrowsize=20, arrowstyle='->')
        nx.draw_networkx_labels(H, pos, labels=node_labels, font_size=8, font_weight='bold')
        
        plt.title(f"Top {top_k} Central Nodes: {name}", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        # Lưu hình
        filename = f"subgraph_{name.replace(' ', '_').replace('-', '_').lower()}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
        
        print(f"💾 Saved visualization: {filename}")
        
    except Exception as e:
        print(f"❌ Error visualizing {name}: {e}")
        import traceback
        traceback.print_exc()


def analyze_graph(G: nx.DiGraph, name="Graph"):
    """Phân tích graph với error handling tốt hơn"""
    import networkx as nx
    from networkx.algorithms.components import strongly_connected_components

    if G.number_of_nodes() == 0:
        return {
            "Graph Name": name,
            "Number of Nodes": 0,
            "Number of Edges": 0,
            "Average Degree": 0,
            "Top 5 Central Nodes": [],
            "Number of 'is-a' Relationships": 0,
            "Number of 'part-of' Relationships": 0,
            "Diameter of Largest SCC": "Empty graph",
            "Clustering Coefficient": 0,
            "Density": 0,
            "Number of Strongly Connected Components": 0,
            "Average In-Degree": 0,
            "Average Out-Degree": 0,
            "Indirect-to-Direct Ratio": 0,
        }

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    avg_degree = sum(dict(G.degree()).values()) / num_nodes if num_nodes > 0 else 0

    # Trung tâm hóa
    try:
        degree_centrality = nx.degree_centrality(G)
        top_5 = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # SỬA LỖI: Safe access to node names với renamed attributes
        top_5_with_names = []
        for node_id, score in top_5:
            node_name = G.nodes[node_id].get("node_name", f"Node_{node_id}")  # Changed from "name"
            if not node_name or node_name == f"Node_{node_id}":
                # Try other properties
                props = G.nodes[node_id]
                node_name = (props.get("title", "") or 
                           props.get("label", "") or 
                           f"Node_{node_id}")
            top_5_with_names.append((node_name, round(score, 3)))
            
    except Exception as e:
        print(f"⚠️ Error calculating centrality for {name}: {e}")
        top_5_with_names = [("Error", 0)]

    # SỬA LỖI: Quan hệ bản chất - sử dụng renamed attribute
    is_a_types = {"hasDegree", "hasType", "isTypeOf", "hasCategory", "subClassOf"}
    part_of_types = {"hasDepartment", "hasFaculty", "hasCampus", "partOf", "locatedIn", "managedBy", "hasBuilding"}

    is_a_count = sum(1 for _, _, d in G.edges(data=True) if d.get("edge_type") in is_a_types)  # Changed from "type"
    part_of_count = sum(1 for _, _, d in G.edges(data=True) if d.get("edge_type") in part_of_types)  # Changed from "type"

    # SCC analysis
    try:
        sccs = list(strongly_connected_components(G))
        scc_count = len(sccs)
        largest_scc = max(sccs, key=len) if sccs else set()
        
        if len(largest_scc) > 1:
            subG = G.subgraph(largest_scc)
            try:
                if nx.is_strongly_connected(subG):
                    diameter = nx.diameter(subG)
                else:
                    diameter = nx.diameter(subG.to_undirected()) if nx.is_connected(subG.to_undirected()) else "Không liên thông"
            except:
                diameter = "Không tính được"
        else:
            diameter = "SCC quá nhỏ"
    except Exception as e:
        print(f"⚠️ Error calculating SCC for {name}: {e}")
        scc_count = 0
        diameter = "Lỗi"

    # Other metrics
    try:
        clustering = round(nx.average_clustering(G.to_undirected()), 3)
    except:
        clustering = 0
        
    density = round(nx.density(G), 3)

    # Degree analysis
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())
    avg_in = sum(in_degrees.values()) / num_nodes
    avg_out = sum(out_degrees.values()) / num_nodes
    indirect_to_direct_ratio = round(avg_in / avg_out, 3) if avg_out > 0 else "Không xác định"

    return {
        "Graph Name": name,
        "Number of Nodes": num_nodes,
        "Number of Edges": num_edges,
        "Average Degree": round(avg_degree, 2),
        "Top 5 Central Nodes": top_5_with_names,
        "Number of 'is-a' Relationships": is_a_count,
        "Number of 'part-of' Relationships": part_of_count,
        "Diameter of Largest SCC": diameter,
        "Clustering Coefficient": clustering,
        "Density": density,
        "Number of Strongly Connected Components": scc_count,
        "Average In-Degree": round(avg_in, 2),
        "Average Out-Degree": round(avg_out, 2),
        "Indirect-to-Direct Ratio": indirect_to_direct_ratio,
    }


def main_analysis():
    """Main function để chạy phân tích"""
    
    # Cấu hình Neo4j
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "123456789"  # Thay đổi password của bạn
    
    # Đọc và phân tích từ Neo4j
    print("🚀 Starting graph analysis from Neo4j...")
    
    ds = build_and_visualize_graph_from_neo4j(
        "SGU - DeepSeek", NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, "deepseek"
    )
    
    gm = build_and_visualize_graph_from_neo4j(
        "SGU - Gemini", NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, "gemini"
    )
    
    op = build_and_visualize_graph_from_neo4j(
        "SGU - OpenAI", NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, "openai"
    )
    
    # Phân tích graphs
    print("\n📊 Analyzing graphs...")
    analyze_deepseek = analyze_graph(ds, "SGU - DeepSeek")
    analyze_gemini = analyze_graph(gm, "SGU - Gemini") 
    analyze_openai = analyze_graph(op, "SGU - OpenAI")
    
    # Tạo DataFrame từ kết quả phân tích
    df_analysis = pd.DataFrame([analyze_deepseek, analyze_gemini, analyze_openai])
    df_analysis.set_index("Graph Name", inplace=True)
    df_analysis = df_analysis.T
    df_analysis.columns = ["SGU - DeepSeek", "SGU - Gemini", "SGU - OpenAI"]
    df_analysis = df_analysis.fillna("Không có dữ liệu")
    
    # Convert to string for display, but keep numeric for plotting
    df_analysis_display = df_analysis.astype(str)
    
    # Xuất DataFrame ra file csv
    df_analysis_display.to_csv("graph_analysis_from_neo4j.csv", encoding="utf-8-sig")
    print("\n--- Kết quả phân tích đồ thị từ Neo4j ---")
    print(df_analysis_display)
    
    # Prepare numeric data for plotting
    try:
        df_numeric = df_analysis.drop(index=[
            "Top 5 Central Nodes",
            "Diameter of Largest SCC", 
            "Indirect-to-Direct Ratio"
        ], errors="ignore")
        
        # Convert to numeric, replacing non-numeric with NaN
        for col in df_numeric.columns:
            df_numeric[col] = pd.to_numeric(df_numeric[col], errors='coerce')
        
        df_numeric = df_numeric.fillna(0)
        
        create_visualizations(df_numeric)
        
    except Exception as e:
        print(f"⚠️ Error creating visualizations: {e}")
        import traceback
        traceback.print_exc()


def create_visualizations(df_numeric):
    """Tạo các biểu đồ so sánh"""
    import matplotlib.pyplot as plt
    
    # Section A: Basic Structure
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))
    axes = axes.flatten()
    basic_metrics = ["Number of Nodes", "Number of Edges", "Average Degree", "Density"]
    
    available_basic = [m for m in basic_metrics if m in df_numeric.index]
    
    for i, metric in enumerate(available_basic):
        if i < len(axes):
            ax = axes[i]
            df_numeric.loc[metric].plot(kind='bar', ax=ax, color=['skyblue', 'lightgreen', 'salmon'])
            ax.set_title(metric, fontsize=12, fontweight='bold')
            ax.set_ylabel("Value")
            ax.set_xticklabels(df_numeric.columns, rotation=45)
            ax.grid(axis='y', alpha=0.3)
            
            # Add value labels on bars
            for j, v in enumerate(df_numeric.loc[metric]):
                if pd.notna(v) and v != 0:
                    ax.text(j, v, f'{v:.2f}' if v < 10 else f'{v:.0f}', 
                           ha='center', va='bottom', fontweight='bold')
    
    # Hide unused subplots
    for i in range(len(available_basic), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.show()
    
    # Section B: Extended Structure & Semantics
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(15, 12))
    axes = axes.flatten()
    extended_metrics = [
        "Clustering Coefficient", "Number of Strongly Connected Components", 
        "Average In-Degree", "Average Out-Degree", 
        "Number of 'is-a' Relationships", "Number of 'part-of' Relationships"
    ]
    
    available_extended = [m for m in extended_metrics if m in df_numeric.index]
    colors = ['skyblue', 'lightgreen', 'salmon', 'orange', 'plum', 'lightgray']
    
    for i, metric in enumerate(available_extended):
        if i < len(axes):
            ax = axes[i]
            df_numeric.loc[metric].plot(kind='bar', ax=ax, color=colors)
            ax.set_title(metric, fontsize=12, fontweight='bold')
            ax.set_ylabel("Value")
            ax.set_xticklabels(df_numeric.columns, rotation=45)
            ax.grid(axis='y', alpha=0.3)
            
            # Add value labels on bars
            for j, v in enumerate(df_numeric.loc[metric]):
                if pd.notna(v) and v != 0:
                    ax.text(j, v, f'{v:.3f}' if v < 1 else f'{v:.0f}', 
                           ha='center', va='bottom', fontweight='bold')
    
    # Hide unused subplots
    for i in range(len(available_extended), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plt.show()


# Chạy phân tích chính
if __name__ == "__main__":
    main_analysis()