from matplotlib import pyplot as plt
from rdflib import Graph, Literal
from sklearn.metrics import auc, precision_score, recall_score, f1_score, accuracy_score, roc_curve
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from rdflib.namespace import RDF, RDFS
import re
import networkx as nx
import json


# Load mô hình embedding
model = SentenceTransformer('all-MiniLM-L6-v2')
# Câu hỏi và đáp án chuẩn
with open("../QC/CQ_SGU.txt", "r", encoding="utf-8") as f:
    questions = [line.strip() for line in f.readlines() if line.strip()]

answers_split = [
    "Trường Đại học Sài Gòn là cơ sở giáo dục đại học công lập trực thuộc Ủy ban Nhân dân TP. Hồ Chí Minh.",
    "Trường chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo.",
    "Trường đào tạo theo hai phương thức: chính quy và giáo dục thường xuyên (bao gồm vừa làm vừa học, văn bằng hai, liên thông).",
    "Trường có 05 chuyên ngành đào tạo tiến sĩ, 12 chuyên ngành cao học và 39 chương trình đào tạo trình độ đại học.",
    "Các lĩnh vực đào tạo chính bao gồm: Kinh tế, Kỹ thuật, Công nghệ, Văn hóa xã hội, Chính trị, Nghệ thuật và Sư phạm.",
    "Có. Trường được cấp Giấy chứng nhận kiểm định chất lượng giáo dục ngày 13/5/2017.",
    "Trường đào tạo 39 ngành trình độ đại học như: Giáo dục Chính trị, Du lịch, Mầm non, Kế toán, Tiểu học, Khoa học Môi trường, Âm nhạc, Kinh doanh Quốc tế, v.v.",
    "Chương trình chất lượng cao hiện tại là ngành Công nghệ Thông tin.",
    "Các ngành sau đại học gồm: Hóa hữu cơ, Hóa lý thuyết và Hóa lý, Khoa học Máy tính, Toán Giải tích, Lịch sử Việt Nam, Văn học Việt Nam, v.v.",
    "Trình độ tiến sĩ đào tạo các ngành: Hóa hữu cơ, Lịch sử Việt Nam, Quản lý Giáo dục, Toán Giải tích, Quản trị Kinh doanh.",
    "Giáo dục thường xuyên gồm: liên thông, vừa làm vừa học, bằng hai.",
    "Văn bằng hai gồm: Ngôn ngữ Anh, Kế toán, Luật, Quản trị Kinh doanh, Giáo dục Tiểu học và Quản lý Giáo dục.",
    "Có 3 cơ sở chính: 273 An Dương Vương (42.743m²), 105 Bà Huyện Thanh Quan (4.823m²), 04 Tôn Đức Thắng (19.655m²).",
    "Ký túc xá tại 99 An Dương Vương, Quận 8, diện tích 4.800m².",
    "Trường hợp tác với các quốc gia như Hoa Kỳ, Anh, Pháp, Nga, Singapore, Áo, Đài Loan, v.v.",
    "Chương trình Cử nhân Quốc tế liên kết với IMC Krems (Áo).",
    "Chương trình tiếng Hoa hợp tác với Trung tâm Hoa ngữ Sư phạm Đài Loan.",
    "Học bổng tiêu biểu: Bộ Y tế Singapore (Asian Nursing), Bộ Giáo dục Đài Loan.",
    "Liên kết đào tạo với Đại học Huddersfiled (Anh) ngành CNTT, TESOL, v.v.",
    "Điều kiện: học lực trung bình trở lên, không bị kỷ luật, không vi phạm quy định.",
    "Quyền lợi: được hỗ trợ kinh phí, cấp chứng nhận, cộng điểm rèn luyện, xét thưởng.",
    "Bài báo đăng tạp chí chuyên ngành hoặc kỷ yếu hội thảo đều được xét thưởng.",
    "Chi tiết NCKH xem tại Quy chế chương 7 hoặc hỏi giảng viên trợ lý NCKH.",
    "ISSN tạp chí: 1859-3208. Website: http://sj.sgu.edu.vn",
    "Phục vụ cán bộ, giảng viên, sinh viên các trường, viện, học viện.",
    "Tạp chí công bố kết quả nghiên cứu, bài giảng dạy - học tập.",
    "Nội dung: mục tiêu, kết quả mới, giá trị thực tiễn, phải được phản biện.",
    "Chuẩn trích dẫn: IEEE cho KHTN, APA cho KHXH và GD.",
    "Yêu cầu minh họa: 300dpi, định dạng JPG, PNG, BMP.",
    "Không phiên âm/dịch tên nước ngoài, phải nêu rõ nguồn và mã đề tài."
]



# Đánh giá thống kê độ đo thống kê (bao nhiêu đỉnh, cạnh, node trung tâm, group [quan hệ is a, part of, ...]).
# đánh giá độ phức tạp
# độ độ gián tiếp  / độ độ trực tiếp 




def build_and_visualize_graph(name, node_file, edge_file):
    def safe_fix_properties(prop_str):
        if not isinstance(prop_str, str) or not prop_str.strip():
            return {}
        pairs = []
        for pair in re.findall(r'(\w+):([^,{}]+)', prop_str):
            key, value = pair
            key = key.strip().strip('"')
            value = value.strip().strip('"')
            pairs.append(f'"{key}": "{value}"')
        json_str = "{" + ", ".join(pairs) + "}"
        return json.loads(json_str)

    def parse_labels(label_str):
        return [label.strip(" '\"") for label in label_str.strip("[]").split(",") if label.strip()]

    # 1. Đọc và xử lý dữ liệu
    nodes_df = pd.read_csv(node_file)
    edges_df = pd.read_csv(edge_file)

    nodes_df["labels"] = nodes_df["labels"].apply(parse_labels)
    nodes_df["properties"] = nodes_df["properties"].apply(safe_fix_properties)
    edges_df["properties"] = edges_df["properties"].apply(safe_fix_properties)

    # 2. Tạo đồ thị
    G = nx.DiGraph()
    for _, row in nodes_df.iterrows():
        props = row["properties"]
        G.add_node(str(row["id"]),
                   labels=row["labels"],
                   name=props.get("name", ""),
                   description=props.get("description", ""))

    for _, row in edges_df.iterrows():
        G.add_edge(str(row["source"]), str(row["target"]),
                   type=row["type"],
                   **row["properties"])

    # 3. Vẽ subgraph 20 node trung tâm
    top_nodes = sorted(nx.degree_centrality(G).items(), key=lambda x: x[1], reverse=True)[:20]
    top_node_ids = [n for n, _ in top_nodes]
    H = G.subgraph(top_node_ids)

    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(H, seed=42)
    node_labels = {n: G.nodes[n].get("name", n) for n in H.nodes}
    nx.draw(H, pos, with_labels=False, node_size=600, node_color="lightblue", edge_color="gray")
    nx.draw_networkx_labels(H, pos, labels=node_labels, font_size=8)
    plt.title(f"Đồ thị con gồm 20 node trung tâm: {name}")
    plt.tight_layout()
    plt.show()

    return G  # trả về graph nếu bạn muốn phân tích tiếp


def analyze_graph(G: nx.DiGraph, name="Graph"):
    import networkx as nx
    from networkx.algorithms.components import strongly_connected_components

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    avg_degree = sum(dict(G.degree()).values()) / num_nodes if num_nodes > 0 else 0

    # Trung tâm hóa
    degree_centrality = nx.degree_centrality(G)
    top_5 = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]

    # Quan hệ bản chất (tự định nghĩa)
    is_a_types = {"hasDegree", "hasType", "isTypeOf", "hasCategory"}
    part_of_types = {"hasDepartment", "hasFaculty", "hasCampus", "partOf", "locatedIn", "managedBy"}

    is_a_count = sum(1 for _, _, d in G.edges(data=True) if d.get("type") in is_a_types)
    part_of_count = sum(1 for _, _, d in G.edges(data=True) if d.get("type") in part_of_types)

    # Đánh giá phức tạp
    largest_scc = max(strongly_connected_components(G), key=len)
    subG = G.subgraph(largest_scc)

    try:
        diameter = nx.diameter(subG.to_undirected()) if len(subG) > 1 and nx.is_connected(subG.to_undirected()) else "Không tính được"
    except:
        diameter = "Lỗi khi tính"

    clustering = round(nx.average_clustering(G.to_undirected()), 3)
    density = round(nx.density(G), 3)
    scc_count = nx.number_strongly_connected_components(G)

    # Độ độ gián tiếp / trực tiếp
    in_degrees = dict(G.in_degree())
    out_degrees = dict(G.out_degree())
    avg_in = sum(in_degrees.values()) / num_nodes
    avg_out = sum(out_degrees.values()) / num_nodes
    indirect_to_direct_ratio = round(avg_in / avg_out, 3) if avg_out > 0 else "Không xác định"

    return {
        "Tên đồ thị": name,
        "Số đỉnh": num_nodes,
        "Số cạnh": num_edges,
        "Bậc trung bình": round(avg_degree, 2),
        "Top 5 trung tâm": [(G.nodes[n]["name"], round(score, 3)) for n, score in top_5],
        "Số quan hệ is-a": is_a_count,
        "Số quan hệ part-of": part_of_count,
        "Đường kính SCC lớn nhất": diameter,
        "Clustering coefficient": clustering,
        "Mật độ (Density)": density,
        "Số thành phần liên thông mạnh": scc_count,
        "In-degree trung bình": round(avg_in, 2),
        "Out-degree trung bình": round(avg_out, 2),
        "Tỷ lệ gián tiếp/trực tiếp": indirect_to_direct_ratio,
    }


# Đọc và xử lý dữ liệu
ds = build_and_visualize_graph("SGU - DeepSeek", "./node_egdes/deepseek_0324/node.csv", "./node_egdes/deepseek_0324/relationship.csv")
gm = build_and_visualize_graph("SGU - Gemini", "./node_egdes/gemini_thinking/node.csv", "./node_egdes/gemini_thinking/relationship.csv")
op = build_and_visualize_graph("SGU - OpenAI", "./node_egdes/openai_4o-mini/node.csv", "./node_egdes/openai_4o-mini/relationship.csv")


# analyze_deepseek = analyze_graph(ds, "SGU - DeepSeek")
# analyze_gemini = analyze_graph(gm, "SGU - Gemini") 
# analyze_openai = analyze_graph(op, "SGU - OpenAI")


# # Tạo DataFrame từ kết quả phân tích
# df_analysis = pd.DataFrame([analyze_deepseek, analyze_gemini, analyze_openai])
# df_analysis.set_index("Tên đồ thị", inplace=True)
# df_analysis = df_analysis.T
# df_analysis.columns = ["SGU - DeepSeek", "SGU - Gemini", "SGU - OpenAI"]
# df_analysis = df_analysis.fillna("Không liên thông")
# df_analysis = df_analysis.astype(str)

# # Xuất DataFrame ra file csv
# df_analysis.to_csv("graph_analysis.csv", encoding="utf-8-sig")
# print("\n--- Kết quả phân tích đồ thị ---")
# print(df_analysis)


def get_best_literal_and_score(G, answer):
    emb_ans = model.encode(answer, convert_to_tensor=True)
    best_score = 0.0
    best_literal = ""
    for _, data in G.nodes(data=True):
        name = data.get("name", "")
        desc = data.get("description", "")
        literal = f"{name}. {desc}".strip()
        if literal:
            emb_literal = model.encode(literal, convert_to_tensor=True)
            score = float(util.cos_sim(emb_ans, emb_literal)[0][0])
            if score > best_score:
                best_score = score
                best_literal = literal
    return best_literal, best_score


def evaluate_semantic_scores_nx(G, answers):
    return [get_best_literal_and_score(G, ans)[1] for ans in answers]

def evaluate_semantic_output_nx(G, answers, threshold=0.6):
    results = []
    for answer in answers:
        literal, score = get_best_literal_and_score(G, answer)
        results.append(literal if score >= threshold else "")
    return results

def evaluate_semantic_match_nx(G, answers, threshold=0.6):
    return [get_best_literal_and_score(G, ans)[1] >= threshold for ans in answers]


def plot_detailed_roc(scores_dict, y_true):
    plt.figure(figsize=(9, 6))
    for label, scores in scores_dict.items():
        fpr, tpr, thresholds = roc_curve(y_true, scores)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f'{label} (AUC = {roc_auc:.2f})')

        # Annotate threshold điểm chính
        for i in range(0, len(thresholds), max(1, len(thresholds)//10)):
            x, y_ = fpr[i], tpr[i]
            thres = round(thresholds[i], 2)
            plt.text(x, y_, str(thres), fontsize=7, alpha=0.6)

    plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
    plt.title("Biểu đồ ROC với điểm đánh dấu Threshold")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def compute_metrics(y_pred):
    y_true = [True] * len(y_pred)
    return {
        "Accuracy": round(accuracy_score(y_true, y_pred), 3),
        "Precision": round(precision_score(y_true, y_pred, zero_division=0), 3),
        "Recall": round(recall_score(y_true, y_pred, zero_division=0), 3),
        "F1 Score": round(f1_score(y_true, y_pred, zero_division=0), 3)
    }

# ===== Thực thi tính toán =====
threshold = 0.6

# Match True/False
y_ds = evaluate_semantic_match_nx(ds, answers_split, threshold=threshold)
y_gm = evaluate_semantic_match_nx(gm, answers_split, threshold=threshold)
y_op = evaluate_semantic_match_nx(op, answers_split, threshold=threshold)

# Literal gần đúng
out_ds = evaluate_semantic_output_nx(ds, answers_split, threshold=threshold)
out_gm = evaluate_semantic_output_nx(gm, answers_split, threshold=threshold)
out_op = evaluate_semantic_output_nx(op, answers_split, threshold=threshold)

# Điểm cosine
scores_dict = {
    "DeepSeek": evaluate_semantic_scores_nx(ds, answers_split),
    "Gemini": evaluate_semantic_scores_nx(gm, answers_split),
    "OpenAI": evaluate_semantic_scores_nx(op, answers_split)
}
y_true = [1] * len(answers_split)
# Đảm bảo y_true có cả 0 và 1 để ROC hoạt động đúng
if len(set(y_true)) == 1:
    y_true.append(0)  # thêm 1 mẫu âm giả
    for label in scores_dict:
        scores_dict[label].append(0.0)  # điểm thấp tương ứng

# Chỉ số tổng hợp
df_semantic_metrics = pd.DataFrame({
    "DeepSeek": compute_metrics(y_ds),
    "Gemini": compute_metrics(y_gm),
    "OpenAI": compute_metrics(y_op)
}).T

# Chi tiết literal
df_detail = pd.DataFrame({
    "Câu hỏi": questions,
    "Đáp án chuẩn": answers_split,
    "DeepSeek trả lời": out_ds,
    "Gemini trả lời": out_gm,
    "OpenAI trả lời": out_op,
    "DeepSeek True/False": y_ds,
    "Gemini True/False": y_gm,
    "OpenAI True/False": y_op
})

# Lưu file
df_semantic_metrics.to_csv("semantic_evaluation_summary.csv", encoding="utf-8-sig")
df_detail.to_csv("semantic_literal_comparison.csv", encoding="utf-8-sig", index=False)

# Vẽ ROC
plot_detailed_roc(scores_dict, y_true)

