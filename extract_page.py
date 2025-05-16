from PyPDF2 import PdfReader, PdfWriter

def extract_pages(input_path, output_path, start_page, end_page):
    """
    Extract a range of pages from input PDF and save to output PDF
    
    Args:
        input_path (str): Path to input PDF file
        output_path (str): Path to save output PDF file
        start_page (int): Starting page number (1-based)
        end_page (int): Ending page number (1-based)
    """
    # Create PDF reader object
    reader = PdfReader(input_path)
    
    # Validate page range
    total_pages = len(reader.pages)
    if start_page < 1 or end_page > total_pages:
        raise ValueError(f"Page range must be between 1 and {total_pages}")
    if start_page > end_page:
        raise ValueError("Start page must be less than or equal to end page")
    
    # Create PDF writer object
    writer = PdfWriter()
    
    # Add the specified pages
    for page_num in range(start_page - 1, end_page):
        writer.add_page(reader.pages[page_num])
    
    # Write the output PDF file
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

if __name__ == "__main__":
    input_pdf = "data/p1.pdf"
    output_pdf = "data/p1_pages1-12.pdf"
    start_page = 5
    end_page = 13
    
    try:
        extract_pages(input_pdf, output_pdf, start_page, end_page)
        print(f"Successfully extracted pages {start_page}-{end_page} to {output_pdf}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")