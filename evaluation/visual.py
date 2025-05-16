import pandas as pd
import matplotlib.pyplot as plt

# Load annotated labels and concept matches
df_labels = pd.read_excel("evaluation_labels_only.xlsx")
df_concepts = pd.read_excel("evaluation_concepts_result.xlsx")

# === Improved Bar Chart: Distribution of CQ answer labels per model with % and counts ===
models = ["DeepSeek", "Gemini", "OpenAI"]
label_stats = []

for model in models:
    counts = df_labels[f"Label_{model}"].value_counts().to_dict()
    counts["Model"] = model
    label_stats.append(counts)

df_stats = pd.DataFrame(label_stats).fillna(0).set_index("Model")
df_stats = df_stats[["Right", "Partial", "Wrong"]]

fig, ax = plt.subplots(figsize=(10, 6))
bottom = [0] * len(df_stats)

colors = {'Right': '#4CAF50', 'Partial': '#FFC107', 'Wrong': '#F44336'}

for label in df_stats.columns:
    values = df_stats[label]
    ax.bar(df_stats.index, values, bottom=bottom, label=label, color=colors[label])
    for i, (val, btm) in enumerate(zip(values, bottom)):
        total = df_stats.iloc[i].sum()
        percent = val / total * 100
        text_color = 'white' if label != 'Partial' else 'black'
        ax.text(i, btm + val / 2, f"{percent:.1f}%\n({int(val)})",
                ha='center', va='center', color=text_color, fontsize=9, fontweight='bold')
    bottom = [i + j for i, j in zip(bottom, values)]

ax.set_title("Distribution of CQ Answer Labels (Right / Partial / Wrong) per Model", fontsize=14)
ax.set_ylabel("Number of Answers")
ax.set_xlabel("Model")
ax.legend(title="Label", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("label_distribution_chart_pct_improved.png")
plt.show()

# === Improved Bar Chart: Concept Match Rate with % ===
match_stats = df_concepts.groupby("Mô hình")["Khớp"].agg(["sum", "count"])
match_stats["Match Rate (%)"] = 100 * match_stats["sum"] / match_stats["count"]

ax2 = match_stats["Match Rate (%)"].plot(kind="bar", figsize=(8, 5), color="seagreen")
for i, val in enumerate(match_stats["Match Rate (%)"]):
    ax2.text(i, val + 1, f"{val:.1f}%", ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.title("Concept Match Rate in Answers per Model", fontsize=14)
plt.ylabel("Match Rate (%)")
plt.xlabel("Model")
plt.ylim(0, 105)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("concept_match_chart_pct_improved.png")
plt.show()
