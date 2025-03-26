# import pdfplumber
# import re
# import os

# # Đường dẫn file PDF
# pdf_path = "./data/p1.pdf"
# text_by_page = []

# # Đọc nội dung PDF, bỏ qua 4 trang đầu
# with pdfplumber.open(pdf_path) as pdf:
#     for i, page in enumerate(pdf.pages[4:]):
#         text = page.extract_text()
#         if text:
#             text_by_page.append(text)

# # Ghép nội dung thành một chuỗi duy nhất
# full_text = "\n".join(text_by_page)

# # Loại bỏ các số trang đơn lẻ xuất hiện cuối đoạn văn
# full_text_cleaned = re.sub(r'\n\d+\s*$', '', full_text, flags=re.MULTILINE)

# with open("./dataset/full_text.txt", "w", encoding="utf-8") as f:
#     f.write(full_text_cleaned)


from PyPDF2 import PdfReader, PdfWriter

input_pdf = PdfReader(open("./data/p1.pdf", "rb"))
pdf_writer = PdfWriter()

# Giả sử bạn muốn tách 20 trang đầu (trang 1 đến trang 20)
# Lưu ý: pages trong PdfReader đánh chỉ số từ 0
for page_num in range(4, 13):  # 0 đến 19, tương đương trang 1-20
    pdf_writer.add_page(input_pdf.pages[page_num])

with open("./dataset/cut.pdf", "wb") as out_file:
    pdf_writer.write(out_file)
