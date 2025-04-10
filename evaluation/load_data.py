import glob

all_text = ""

for file_path in glob.glob("./dataset/PHẦN 1_section_*.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        all_text += "\n" + text

