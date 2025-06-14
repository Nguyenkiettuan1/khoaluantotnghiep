import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Tuple, Optional

def load_evaluation_data(labels_file: str = "evaluation_labels_only.xlsx", 
                        concepts_file: str = "evaluation_concepts_result.xlsx") -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """Load evaluation data files"""
    df_labels = None
    df_concepts = None
    
    if os.path.exists(labels_file):
        df_labels = pd.read_excel(labels_file)
    else:
        print(f"Warning: Labels file not found: {labels_file}")
    
    if os.path.exists(concepts_file):
        df_concepts = pd.read_excel(concepts_file)
    else:
        print(f"Warning: Concepts file not found: {concepts_file}")
    
    return df_labels, df_concepts

def create_label_distribution_chart(df_labels: pd.DataFrame, output_dir: str = "evaluation_charts") -> str:
    """Create label distribution chart for Q&A answers"""
    os.makedirs(output_dir, exist_ok=True)
    
    models = ["DeepSeek", "Gemini", "OpenAI"]
    label_stats = []

    for model in models:
        if f"Label_{model}" in df_labels.columns:
            counts = df_labels[f"Label_{model}"].value_counts().to_dict()
            counts["Model"] = model
            label_stats.append(counts)

    if not label_stats:
        print("Warning: No label data found for any model")
        return ""

    df_stats = pd.DataFrame(label_stats).fillna(0).set_index("Model")
    df_stats = df_stats[["Right", "Partial", "Wrong"]]        # bảo đảm đúng thứ tự

    fig, ax = plt.subplots(figsize=(10, 6))
    bottom = [0] * len(df_stats)
    colors = {'Right': '#4CAF50', 'Partial': '#FFC107', 'Wrong': '#F44336'}

    for label in df_stats.columns:
        values = df_stats[label]
        ax.bar(df_stats.index, values, bottom=bottom, label=label, color=colors[label])

        # Nhãn % + (số) trong miếng
        for i, (val, btm) in enumerate(zip(values, bottom)):
            total = df_stats.iloc[i].sum()
            if total > 0:
                percent = val / total * 100
                text_color = 'white' if label != 'Partial' else 'black'
                ax.text(i, btm + val / 2,
                        f"{percent:.1f}%\n({int(val)})",
                        ha='center', va='center', color=text_color, fontsize=9,
                        fontweight='bold')
        bottom = [i + j for i, j in zip(bottom, values)]

    # ----- Dòng tổng Right / Partial / Wrong trên cùng -----
    for i, model in enumerate(df_stats.index):
        r, p, w = df_stats.loc[model]
        total_height = df_stats.loc[model].sum()
        ax.text(i, total_height + 0.5,
                f"R:{int(r)} | P:{int(p)} | W:{int(w)}",
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_title("Distribution of CQ Answer Labels per Model", fontsize=14)
    ax.set_ylabel("Number of Answers")
    ax.set_xlabel("Model")
    ax.legend(title="Label", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, "label_distribution_chart_pct_improved.png")
    plt.savefig(output_path)
    plt.close()
    
    return output_path

def create_concept_match_chart(df_concepts: pd.DataFrame, output_dir: str = "evaluation_charts") -> str:
    """Create concept match rate chart"""
    os.makedirs(output_dir, exist_ok=True)
    
    if "Mô hình" not in df_concepts.columns or "Khớp" not in df_concepts.columns:
        print("Warning: Required columns 'Mô hình' or 'Khớp' not found in concepts data")
        return ""
    
    match_stats = df_concepts.groupby("Mô hình")["Khớp"].agg(["sum", "count"])
    match_stats["Match Rate (%)"] = 100 * match_stats["sum"] / match_stats["count"]

    fig, ax2 = plt.subplots(figsize=(8, 5))
    bars = ax2.bar(match_stats.index, match_stats["Match Rate (%)"], color="seagreen")

    # Nhãn % + (sum / count)
    for i, (val, (s, c)) in enumerate(zip(match_stats["Match Rate (%)"],
                                          match_stats[["sum", "count"]].itertuples(index=False))):
        ax2.text(i, val + 1.5,
                 f"{val:.1f}%\n({int(s)}/{int(c)})",
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax2.set_title("Concept Match Rate in Answers per Model", fontsize=14)
    ax2.set_ylabel("Match Rate (%)")
    ax2.set_xlabel("Model")
    ax2.set_ylim(0, 110)
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, "concept_match_chart_pct_improved.png")
    plt.savefig(output_path)
    plt.close()
    
    return output_path

def create_all_visualizations(labels_file: str = "evaluation_labels_only.xlsx", 
                             concepts_file: str = "evaluation_concepts_result.xlsx",
                             output_dir: str = "evaluation_charts") -> list:
    """Create all visualization charts"""
    df_labels, df_concepts = load_evaluation_data(labels_file, concepts_file)
    created_charts = []
    
    if df_labels is not None:
        chart_path = create_label_distribution_chart(df_labels, output_dir)
        if chart_path:
            created_charts.append(chart_path)
            print(f"✅ Created label distribution chart: {chart_path}")
    
    if df_concepts is not None:
        chart_path = create_concept_match_chart(df_concepts, output_dir)
        if chart_path:
            created_charts.append(chart_path)
            print(f"✅ Created concept match chart: {chart_path}")
    
    return created_charts

def main():
    """Main function to run when script is executed directly"""
    print("🎨 Creating evaluation visualizations...")
    
    # Try current directory first, then evaluation_results
    for base_dir in [".", "evaluation_results"]:
        labels_file = os.path.join(base_dir, "evaluation_labels_only.xlsx")
        concepts_file = os.path.join(base_dir, "evaluation_concepts_result.xlsx")
        
        if os.path.exists(labels_file) or os.path.exists(concepts_file):
            created = create_all_visualizations(labels_file, concepts_file)
            if created:
                print(f"✅ Created {len(created)} charts successfully!")
                return
    
    print("❌ No evaluation data files found. Please run evaluation pipeline first.")

if __name__ == "__main__":
    main()
