import pdfplumber
import re
import os

# Đường dẫn file PDF
pdf_path = "./data/p1.pdf"
text_by_page = []

# Đọc nội dung PDF, bỏ qua 4 trang đầu
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages[4:]):
        text = page.extract_text()
        if text:
            text_by_page.append(text)

# Ghép nội dung thành một chuỗi duy nhất
full_text = "\n".join(text_by_page)

# Loại bỏ các số trang đơn lẻ xuất hiện cuối đoạn văn
full_text_cleaned = re.sub(r'\n\d+\s*$', '', full_text, flags=re.MULTILINE)

with open("./dataset/full_text.txt", "w", encoding="utf-8") as f:
    f.write(full_text_cleaned)


# Tách nội dung thành các phần dựa trên "PHẦN" và số phần
split_sections = re.split(r"(PHẦN\s+\d+)", full_text_cleaned)

# Tạo thư mục lưu trữ nếu chưa có
os.makedirs("./dataset", exist_ok=True)

# Xử lý từng phần
for i in range(1, len(split_sections), 2):
    section_title = split_sections[i].strip()
    section_content = split_sections[i + 1].strip() if i + 1 < len(split_sections) else ""

    # Tách các mục nhỏ theo I., II., III.,...
    subsections = re.split(r"\n(I{1,3}|IV|V|VI|VII|VIII|IX|X)\.\s+", section_content)

    # Ghép tiêu đề với nội dung của từng mục nhỏ
    for j in range(1, len(subsections), 2):
        subsection_title = subsections[j].strip()
        subsection_content = subsections[j + 1].strip() if j + 1 < len(subsections) else ""

        # Tên file lưu: phần + mục nhỏ
        file_path = f"./dataset/{section_title}_section_{subsection_title}.txt"

        # Lưu vào file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"{section_title} - {subsection_title}\n\n{subsection_content}")

        print(f"✅ Đã lưu: {file_path}")


