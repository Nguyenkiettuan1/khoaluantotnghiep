import re

def clean_cypher_code(cypher_code: str, remove_trailing_dot: bool = True) -> str:
    """
    Làm sạch mã Cypher:
    - Loại bỏ markdown code block nếu có.
    - Loại bỏ dòng trống và khoảng trắng thừa.
    - Nếu remove_trailing_dot=True, loại bỏ dấu chấm thừa ở cuối mỗi dòng (trừ dòng comment).
    
    Tham số:
    - cypher_code: chuỗi mã Cypher cần làm sạch.
    - remove_trailing_dot: nếu True, xóa dấu chấm cuối dòng (mặc định là True).
    
    Trả về chuỗi mã Cypher đã được làm sạch.
    """
    # Loại bỏ markdown nếu có
    cypher_code = cypher_code.strip()
    if cypher_code.startswith("```"):
        cypher_code = cypher_code.strip("```").strip()
    
    # Tách các dòng và loại bỏ dòng trống
    lines = [line.strip() for line in cypher_code.splitlines() if line.strip()]
    
    cleaned_lines = []
    for line in lines:
        # Nếu dòng không phải là comment và remove_trailing_dot là True,
        # loại bỏ dấu chấm thừa ở cuối dòng
        if remove_trailing_dot and not line.startswith("//"):
            line = re.sub(r'\.\s*$', '', line)
        cleaned_lines.append(line)
    
    # Ghép lại các dòng đã xử lý thành một chuỗi
    final_code = "\n".join(cleaned_lines)
    return final_code.strip()



