# Tài liệu Dự án

Dự án này bao gồm các module thực hiện các chức năng chính như sau:
- **extract_data**: Cắt và lấy dữ liệu từ file PDF.
- **neoj4connector**: Kết nối đến cơ sở dữ liệu Neo4j và chạy các truy vấn Cypher được generate.
- **run.py**: Sinh ra truy vấn Cypher dựa trên dữ liệu đã thu thập và lưu lại tại thư mục `cypher`.
- **utils**: Sinh ra file TTL từ dữ liệu xử lý.

## Mục đích dự án

Mục tiêu của dự án là tự động hóa quy trình:
1. Trích xuất dữ liệu từ các file PDF.
2. Sinh các truy vấn Cypher để nhập dữ liệu vào cơ sở dữ liệu đồ thị Neo4j.
3. Tạo file TTL phục vụ cho việc chuyển đổi hoặc lưu trữ dữ liệu theo định dạng mong muốn.

## Cấu trúc dự án

- **extract_data**:  
  Module này thực hiện việc cắt và lấy dữ liệu từ file PDF.  
  **Chức năng chính**:  
  - Đọc file PDF.
  - Xử lý và trích xuất thông tin cần thiết.

- **neoj4connector**:  
  File này đảm nhận vai trò kết nối đến Neo4j và chạy các truy vấn Cypher đã được generate.  
  **Chức năng chính**:  
  - Thiết lập kết nối với cơ sở dữ liệu Neo4j.
  - Thực thi các truy vấn Cypher để cập nhật hoặc truy vấn dữ liệu.

- **run.py**:  
  Script chính để sinh ra các truy vấn Cypher dựa trên dữ liệu được trích xuất.  
  **Chức năng chính**:  
  - Tổng hợp dữ liệu đã được lấy từ `extract_data`.
  - Sinh các truy vấn Cypher theo yêu cầu.
  - Lưu các truy vấn vào thư mục `cypher` để tiện cho việc thực thi sau này.

- **utils**:  
  Module tiện ích chịu trách nhiệm sinh ra file TTL.  
  **Chức năng chính**:  
  - Xử lý dữ liệu theo định dạng cần thiết.
  - Sinh ra file TTL từ dữ liệu đã được xử lý.

## Báo cáo về Quy trình Sinh Ontology từ Tài liệu (phần 1 của Dataset)

### 1. Giới thiệu

Báo cáo này mô tả quy trình tạo ontology và xây dựng knowledge graph từ một phần của dataset tài liệu giới thiệu về Trường Đại học Sài Gòn. Trong phần này, chúng tôi tập trung vào nội dung liên quan đến chương trình đào tạo, sinh viên, giảng viên và các hoạt động nghiên cứu, giảng dạy, loại bỏ cấu trúc bộ máy quản lý của trường.

### 2. Quy trình thực hiện

#### 2.1 Sinh tập câu hỏi chọn lọc (Qc)

Sử dụng mô hình ngôn ngữ lớn (LLM) để tạo ra tập hợp các câu hỏi có chọn lọc (Qc) dựa trên nội dung tài liệu đã xử lý.

Các câu hỏi này tập trung vào các chủ đề liên quan đến chương trình đào tạo, giảng viên, sinh viên và hoạt động học thuật của trường.

#### 2.2 Tạo file Ontology (turtle - ttl)

Dựa vào tập câu hỏi Qc, chúng tôi tiến hành thiết kế ontology để biểu diễn các khái niệm và mối quan hệ giữa chúng.

Ontology được viết dưới định dạng Turtle (ttl), gồm các lớp chính như: SinhVien, GiangVien, ChuongTrinhDaoTao, KhoaHoc, HoatDongNghienCuu.

Ontology được xây dựng và kiểm tra bằng công cụ Protégé để đảm bảo cấu trúc chuẩn và logic chặt chẽ.

#### 2.3 Chunking và sinh câu Cypher thông qua LLM

Dữ liệu từ tài liệu giới thiệu được chia nhỏ thành các đoạn văn bản (chunks), mỗi chunk khoảng 3.000 từ.

Các đoạn văn bản này được xử lý thông qua LLM (mô hình GPT4o-mini) để sinh ra các câu truy vấn Cypher, giúp chuyển đổi dữ liệu văn bản thành dạng đồ thị theo ontology đã tạo.

#### 2.4 Xây dựng Knowledge Graph trên Neo4j

Sau khi hoàn thành việc chạy toàn bộ các đoạn văn bản (chunks) qua mô hình, dữ liệu được đưa vào Neo4j thông qua các câu truy vấn Cypher đã sinh.

Kết quả là một knowledge graph hoàn chỉnh, thể hiện rõ ràng các mối quan hệ và khái niệm theo đúng cấu trúc của ontology.

### 3. Kết quả đạt được

Ontology đã tạo thành công với đầy đủ các lớp và thuộc tính liên quan đến các đối tượng đào tạo và học thuật.

Knowledge graph thu được có độ chính xác và logic cao, giúp dễ dàng tra cứu và khai thác thông tin liên quan đến chương trình đào tạo, giảng viên, sinh viên và các hoạt động nghiên cứu.

### 4. Kết luận

Phần 1 của dataset đã được xử lý thành công, hoàn thành các mục tiêu:
- Sinh tập câu hỏi chọn lọc (Qc).
- Tạo ontology mẫu chuẩn định dạng Turtle.
- Sinh và chạy các câu truy vấn Cypher thông qua LLM GPT4o-mini.
- Xây dựng Knowledge Graph hoàn chỉnh trên nền tảng Neo4j.

Phương pháp này đảm bảo việc mở rộng xử lý toàn bộ dataset trong tương lai một cách hiệu quả và nhất quán.

## Hướng dẫn sử dụng

1. **Trích xuất dữ liệu từ PDF**  
   Chạy module `extract_data` để cắt và lấy dữ liệu từ các file PDF.  
   Ví dụ:  
   ```bash
   python extract_data.py --input path/to/pdf
   ```

2. **Sinh truy vấn Cypher**  
   Chạy script `run.py` để sinh ra các truy vấn Cypher dựa trên dữ liệu thu thập.  
   Ví dụ:  
   ```bash
   python run.py
   ```  
   Các truy vấn sẽ được lưu trong thư mục `cypher`.

3. **Kết nối và chạy truy vấn với Neo4j**  
   Sử dụng module `neoj4connector` để kết nối đến cơ sở dữ liệu Neo4j và thực thi các truy vấn đã generate.  
   Ví dụ:  
   ```bash
   python neoj4connector.py --query path/to/cypher/query.cypher
   ```

4. **Tạo file TTL**  
   Chạy module `utils` để sinh ra file TTL từ dữ liệu đã xử lý.  
   Ví dụ:  
   ```bash
   python utils.py --input path/to/data
   ```

## Yêu cầu hệ thống

- Python 3.x
- Các thư viện cần thiết (có thể được cài đặt qua file `requirements.txt`):
  ```bash
  pip install -r requirements.txt
  ```
- Neo4j (với cấu hình kết nối phù hợp, được thiết lập trong `neoj4connector`)
