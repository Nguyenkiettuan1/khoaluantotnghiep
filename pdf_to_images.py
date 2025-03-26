import os
from pdf2image import convert_from_path

def convert_pdf_to_images(pdf_path, output_dir="images", start_page=5, end_page=13):
    """Convert PDF pages to images"""
    # Kiểm tra file PDF
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Không tìm thấy file PDF: {pdf_path}")
    
    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Đường dẫn đến Poppler
        poppler_path = os.path.join(os.getcwd(), "tools", "poppler", "poppler-23.11.0", "Library", "bin")
        
        print(f"Đang xử lý PDF từ trang {start_page} đến trang {end_page}...")
        
        # Chuyển đổi PDF thành ảnh
        images = convert_from_path(
            pdf_path,
            poppler_path=poppler_path,
            first_page=start_page,
            last_page=end_page
        )
        
        # Lưu từng trang
        for i, image in enumerate(images):
            page_num = start_page + i
            output_path = os.path.join(output_dir, f'page_{page_num}.png')
            
            print(f"Đang lưu trang {page_num}...", end='')
            image.save(output_path, 'PNG')
            print(" ✅")
        
        print(f"\n✅ Đã chuyển đổi {len(images)} trang thành công!")
        
    except Exception as e:
        print(f"\n❌ Lỗi khi chuyển đổi PDF: {str(e)}")
        print("\nVui lòng kiểm tra:")
        print(f"1. Poppler đã được cài đặt tại: {poppler_path}")
        print("2. File PDF không bị hỏng hoặc bị khóa")
        raise e

if __name__ == "__main__":
    try:
        convert_pdf_to_images(
            pdf_path="data/p1.pdf",
            output_dir="images",
            start_page=5,
            end_page=13
        )
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")