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



