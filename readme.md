# Hệ thống Vector Search cho Đại học Sài Gòn

## Giới thiệu
Hệ thống tìm kiếm thông minh cho Trường Đại học Sài Gòn sử dụng Vector Search và OpenAI để tạo câu trả lời chính xác từ dữ liệu có cấu trúc.

## Quy trình xây dựng hệ thống

### 1. Chuẩn bị dữ liệu và Ontology

#### a. Xây dựng Competency Questions
```
- Đặt ra các câu hỏi (Q) từ dữ liệu nguồn, bước này có thể sử dụng Chat AI miễn phí để generate ra câu hỏi
- Đưa các câu hỏi đó vào folder QA
QA/
├── QA_SGU_v1.txt          # Các câu hỏi năng lực
└── QA_SGU_v2.txt       # Các câu hỏi năng lực
```

#### b. Tạo Ontology từ Competency Questions
```bash
# Tự động tạo ontology từ câu hỏi năng lực
python utils.py
```
- File ontology được tạo tại: `ontology/ontology_generated.ttl`
- Xác định các lớp (Classes) và mối quan hệ (Relationships)
- Định nghĩa cấu trúc dữ liệu chuẩn

#### c. Chuẩn bị dữ liệu nguồn
Cấu trúc thư mục dataset:
```
dataset/
├── PHẦN 1_section_I.txt
├── PHẦN 1_section_II.txt
├── PHẦN 1_section_III.txt
├── PHẦN 1_section_IV.txt
├── PHẦN 1_section_V.txt
├── PHẦN 1_section_VI.txt
└── ... các file khác
```

### 2. Xây dựng Knowledge Graph

#### a. Sinh Cypher Queries
```bash
python run.py
```
Quá trình này sẽ:
1. **Đọc dữ liệu PHẦN 1**:
   - Chỉ xử lý các file bắt đầu bằng "PHẦN 1" trong thư mục `dataset/`
   - Ví dụ: PHẦN 1_section_I.txt, PHẦN 1_section_II.txt, etc.
   - Bỏ qua các file PHẦN 2 và các file khác

2. **Đọc ontology**:
   - Đọc file `ontology/ontology_generated.ttl`
   - Sử dụng làm cơ sở cho việc sinh Cypher queries

3. **Xử lý dữ liệu**:
   - Chia nhỏ nội dung từng file thành các đoạn 3000 ký tự
   - Đảm bảo không cắt giữa câu hoặc đoạn văn
   - Giúp GPT xử lý hiệu quả hơn

4. **Sinh Cypher queries**:
   - Sử dụng OpenAI API để phân tích từng đoạn
   - Tạo các câu lệnh MERGE phù hợp với ontology
   - Đảm bảo tính nhất quán của dữ liệu

5. **Lưu trữ kết quả**:
   - Kiểm tra và làm sạch mã Cypher
   - Lưu tất cả queries vào `cypher/populate_ontology.cypher`
   - Sẵn sàng cho việc import vào Neo4j

#### b. Import vào Neo4j
```bash

### 3. Xây dựng Vector Index và Embedding

#### a. Kiến trúc hệ thống
```mermaid
graph TD
    A[Dữ liệu Nguồn] --> B[Text Preprocessing]
    B --> C[Embedding Generation]
    C --> D[Vector Index]
    D --> E[Vector Database]
    E --> F[Search API]
    F --> G[Web Interface]

    style A fill:#f9f,stroke:#333
    style E fill:#bbf,stroke:#333
    style G fill:#bfb,stroke:#333
```



2. **Quy trình xử lý truy vấn**:
   ```mermaid
   sequenceDiagram
       User->>+Frontend: Nhập câu hỏi
       Frontend->>+API: POST /api/search
       API->>+Embedding: Tạo vector
       Embedding->>+Vector DB: Tìm kiếm
       Vector DB-->>-API: Kết quả
       API-->>-Frontend: JSON Response
       Frontend-->>-User: Hiển thị kết quả
   ```

