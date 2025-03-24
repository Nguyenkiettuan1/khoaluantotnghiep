# SGU Vector Search System

Hệ thống tìm kiếm thông tin Đại học Sài Gòn sử dụng Vector Search và OpenAI

## Quy trình xây dựng hệ thống

### 1. Trích xuất dữ liệu
1. **Chuẩn bị dữ liệu gốc**:
   - Thu thập thông tin từ website của trường
   - Lưu trữ dữ liệu thô trong thư mục `data/`
   - Định dạng file: PDF, TEXT

2. **Tiền xử lý dữ liệu**:
   ```bash
   # Chạy script trích xuất dữ liệu từ PDF
   python extract_data.py
   ```
   - Script sẽ:
     + Đọc file PDF từ thư mục `data/`
     + Chuyển đổi sang văn bản thuần túy
     + Tách thành các phần nhỏ theo mục
     + Lưu kết quả vào thư mục `dataset/`

3. **Kiểm tra và làm sạch dữ liệu**:
   - Xem lại các file trong `dataset/`
   - Đảm bảo encoding UTF-8
   - Loại bỏ các ký tự đặc biệt không cần thiết

### 2. Chuẩn bị Neo4j Database

1. **Cài đặt Neo4j Enterprise Edition**:
   - Tải và cài đặt Neo4j Enterprise Edition
   - Kích hoạt Vector Search plugin
   - Tạo database mới (nếu cần)

2. **Tạo Schema**:
   - Các node labels:
     + University
     + Department
     + TrainingProgram
     + Campus
     + InternationalCooperation
     + Scholarship
     + ResearchTopic
     + Journal

3. **Tạo Constraints và Indexes**:
   ```cypher
   # Chạy trong Neo4j Browser
   CREATE CONSTRAINT unique_department_name IF NOT EXISTS
   FOR (d:Department) REQUIRE d.name IS UNIQUE;
   
   # Tương tự cho các node khác
   ```

### 3. Import Dữ liệu vào Neo4j

1. **Chuẩn bị Cypher Queries**:
   - File `cypher/populate_ontology.cypher` chứa các câu lệnh import
   - Cấu trúc dữ liệu:
     ```cypher
     MERGE (sgu:University {name: 'Trường Đại học Sài Gòn'})
     MERGE (dept:Department {name: 'Tên Khoa'})
     MERGE (sgu)-[:hasDepartment]->(dept)
     ```

2. **Chạy Import Script**:
   ```bash
   # Clear database (nếu cần)
   python clearCypher.py
   
   # Import dữ liệu
   python run.py
   ```

3. **Kiểm tra dữ liệu**:
   ```cypher
   # Verify data in Neo4j Browser
   MATCH (n) RETURN n LIMIT 25;
   MATCH ()-[r]->() RETURN TYPE(r), COUNT(*);
   ```

### 4. Tạo Vector Embeddings

1. **Cấu hình OpenAI**:
   - Copy `.env.example` thành `.env`
   - Thêm OpenAI API key vào file `.env`

2. **Tạo Vector Indexes**:
   ```bash
   # Chạy ứng dụng
   streamlit run app.py
   ```
   - Hệ thống sẽ tự động:
     + Tạo vector indexes cho mỗi loại node
     + Generate embeddings cho dữ liệu hiện có
     + Lưu embeddings vào Neo4j

3. **Kiểm tra Vector Indexes**:
   ```cypher
   # Verify trong Neo4j Browser
   SHOW INDEXES
   YIELD name, type
   WHERE type = 'VECTOR';
   ```

## Cài đặt | Installation

[Previous installation instructions remain the same...]

## Sử dụng | Usage

[Previous usage instructions remain the same...]

## Cấu trúc dự án | Project Structure
```
project/
├── app.py                         # Streamlit web interface
├── neo4jconnector.py              # Neo4j connection and vector search
├── extract_data.py               # Data extraction script
├── clearCypher.py               # Database clearing utility
├── run.py                       # Data import script
├── requirements.txt              # Project dependencies
├── .env                         # Environment configuration
├── .env.example                 # Environment template
├── data/                        # Raw data directory
│   └── p1.pdf                   # Source PDF files
├── dataset/                     # Processed data
│   └── *.txt                    # Extracted text files
├── cypher/                      # Cypher queries
│   └── populate_ontology.cypher # Data import queries
└── logs/                        # Log files directory
```

[Previous support section remains the same...]
