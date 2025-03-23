# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# load_dotenv()
# # Hãy cài đặt biến môi trường OPENAI_API_KEY hoặc thay bằng chuỗi API Key trực tiếp
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def clean_cypher_code(raw_code: str) -> str:
#     """
#     Gọi LLM (ví dụ GPT) để sửa code Cypher:
#       - Loại bỏ chú thích / giải thích
#       - Gộp MERGE node trùng (VD: university) một lần
#       - Chỉ trả về câu lệnh Cypher thuần
#     """
#     system_prompt = f"""
#     You are ChatGPT, specialized in analyzing and fixing Cypher code for Neo4j. 

#     We have some code (possibly with issues like repeated merges, empty nodes/relationships, or extra text). 
#     Your goals:
#     1. **No node or relationship is empty**:
#     - Every node must have a label and a 'name' property (or similar required properties).
#     - Every relationship must have a type (like [:OFFERS], [:HAS_DEPARTMENT], etc.) and never be empty.
#     2. **Avoid 'Variable already declared'**: 
#     - If a node variable was merged, reuse it instead of merging again.
#     - Each distinct node uses a unique variable; do not reuse the same variable name for different entities.
#     3. **Retain all data**: 
#     - Keep all nodes and relationships from the original. 
#     - If there's repeated merges for the same node, unify them so the node merges once, reusing the variable for relationships.
#     4. **Output only valid Cypher statements** — no explanations or extra text.
#     5. **No node/relationship is lost**: even if code is repetitive, unify it carefully but do not drop data.
#     6. If the code references a node with an empty label or no 'name', fix it by assigning a label or property if logically derivable, or unify with an existing node if duplicates.
#     7. Ensure each node has at least one relationship (no isolated nodes).
#     8. You may use ON CREATE SET / ON MATCH SET if needed to unify properties.

#     Important: 
#     - The final code must be a single or multiple blocks of Cypher that runs without error on Neo4j.
#     - No commentary. Just the corrected/optimized Cypher.
#     """
    
#     user_prompt = f"""
#     Below is some raw Cypher code (or text to produce Cypher). It might have:
#     - Repeated MERGE for the same node variable (causing 'Variable already declared').
#     - Nodes or relationships without label/name/type (empty).
#     - Extra text or explanations.

#     Your task:
#     1. **Ensure no node/relationship is empty** — each node has label + `name`, each relationship has a type.
#     2. **No repeated MERGE**: if the same node is used multiple times, unify them or reuse the same variable. 
#     3. **Keep all data** (no node or relationship is dropped).
#     4. **Use MERGE** to avoid duplicates, plus ON CREATE SET/ON MATCH SET if needed.
#     5. Output only the final Cypher code, no extra text or commentary.
#     6. Guarantee the final code can run on Neo4j with no 'Variable already declared' errors.

#     Raw code or text:
#     ---
#     {raw_code}
#     ---
#     """

    
#     # Gọi OpenAI
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         temperature=0.0,
#         messages=[
#             {"role": "system", "content": system_prompt.strip()},
#             {"role": "user", "content": user_prompt.strip()},
#         ],
#     )
    
#     # Lấy nội dung trả về, bảo đảm chỉ là code Cypher
#     cleaned_code = response.choices[0].message.content.strip()
#     unwanted_keywords = ["```cypher", "```"]
#     for keyword in unwanted_keywords:
#         cleaned_code = cleaned_code.replace(keyword, "")
    
#     return cleaned_code


# import re

# def clean_cypher_code(cypher_code: str) -> str:
#     # Loại bỏ markdown code block nếu có
#     cypher_code = cypher_code.strip()
#     if cypher_code.startswith("```"):
#         cypher_code = cypher_code.strip("```").strip()
    
#     # Tách các dòng và loại bỏ dòng trống
#     lines = cypher_code.splitlines()
#     cleaned_lines = [line.strip() for line in lines if line.strip() != ""]
    
#     # Đảm bảo mỗi dòng kết thúc bằng dấu chấm
#     final_lines = []
#     for line in cleaned_lines:
#         # Loại bỏ dấu chấm thừa nếu có sau khi trim
#         line = line.rstrip()
#         # Nếu dòng không kết thúc bằng dấu chấm và không là comment, thêm dấu chấm
#         if not line.endswith(".") and not line.startswith("//"):
#             line += " ."
#         final_lines.append(line)
    
#     # Ghép lại các dòng, có thể thêm xuống dòng giữa các câu lệnh
#     final_code = "\n".join(final_lines)
#     return final_code.strip()

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



