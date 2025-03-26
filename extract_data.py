import os
import re
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

def extract_text_from_pdf(pdf_path, start_page=4, end_page=13):
    """Extract text from PDF using OCR from specific pages"""
    # Đường dẫn đến các công cụ
    base_dir = os.getcwd()
    poppler_path = os.path.join(base_dir, "tools", "poppler", "poppler-23.11.0", "Library", "bin")
    tesseract_path = os.path.join(base_dir, "tools", "tesseract", "tesseract.exe")
    
    # Hiển thị thông tin
    print(f"Đường dẫn Poppler: {poppler_path}")
    print(f"Đường dẫn Tesseract: {tesseract_path}")
    
    # Thiết lập Tesseract
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    # Chuyển PDF thành hình ảnh
    print(f"\nĐang chuyển PDF thành hình ảnh (trang {start_page + 1} đến {end_page})...")
    try:
        # Convert all pages at once for better performance
        images = convert_from_path(
            pdf_path,
            poppler_path=poppler_path,
            first_page=start_page + 1,  # pdf2image uses 1-based indexing
            last_page=end_page
        )
        print(f"✅ Đã chuyển đổi được {len(images)} trang")
    except Exception as e:
        print(f"❌ Lỗi khi chuyển đổi PDF: {str(e)}")
        raise e
    
    # Xử lý OCR từng trang
    print("\nĐang thực hiện OCR...")
    text_by_page = []
    
    for i, image in enumerate(images):
        current_page = start_page + i + 1
        print(f"Đang xử lý trang {current_page}/{end_page}...", end='')
        
        try:
            # Thực hiện OCR với ngôn ngữ tiếng Việt
            text = pytesseract.image_to_string(image, lang='vie')
            if text.strip():
                text_by_page.append(text)
                print(" ✅")
            else:
                print(" ⚠️ (Không có nội dung)")
        except Exception as e:
            print(f" ❌\nLỗi khi xử lý trang {current_page}: {str(e)}")
            continue
    
    return "\n\n".join(text_by_page)

def save_sections(text):
    """Save extracted text to files"""
    # Tạo thư mục dataset nếu chưa tồn tại
    os.makedirs("./dataset", exist_ok=True)
    
    # Lưu toàn bộ văn bản
    print("\nĐang lưu văn bản đầy đủ...")
    with open("./dataset/full_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("✅ Đã lưu văn bản đầy đủ")
    
    # Tách và lưu từng phần
    print("\nĐang tách và lưu từng phần...")
    sections = re.split(r"(PHẦN\s+\d+)", text)
    
    section_count = 0
    for i in range(1, len(sections), 2):
        section_title = sections[i].strip()
        section_content = sections[i + 1].strip() if i + 1 < len(sections) else ""
        
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
            
            section_count += 1
            print(f"✅ Đã lưu: {file_path}")
    
    print(f"\nHoàn thành! Đã lưu {section_count} phần.")

def main():
    pdf_path = "./data/p1.pdf"
    try:
        # Extract text from PDF
        print("=== BẮT ĐẦU XỬ LÝ PDF ===")
        extracted_text = extract_text_from_pdf(pdf_path, start_page=4, end_page=13)  # Trang 5-13
        
        # Clean text
        print("\nĐang làm sạch văn bản...")
        cleaned_text = re.sub(r'\n\d+\s*$', '', extracted_text, flags=re.MULTILINE)
        
        # Save sections
        save_sections(cleaned_text)
        
        print("\n✅ Hoàn thành toàn bộ quá trình!")
        
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
        print("\nVui lòng kiểm tra:")
        print("1. Đã cài đặt Poppler vào thư mục tools/poppler")
        print("2. Đã cài đặt Tesseract vào thư mục tools/tesseract")
        print("3. Đã có file vie.traineddata trong thư mục tools/tesseract/tessdata")

if __name__ == "__main__":
    main()
