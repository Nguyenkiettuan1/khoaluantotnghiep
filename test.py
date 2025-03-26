from pdf2image import convert_from_path
import pytesseract

def ocr_pdf(pdf_path, dpi=300, lang="vie"):
    pages = convert_from_path(pdf_path, dpi=dpi)
    all_text = ""
    for i, page_img in enumerate(pages):
        ocr_text = pytesseract.image_to_string(page_img, lang=lang)
        all_text += f"\n--- Trang {i+1} ---\n{ocr_text}"
    return all_text

pdf_file = "./dataset/cut.pdf"
text_ocr = ocr_pdf(pdf_file)
print(text_ocr[:1000])
