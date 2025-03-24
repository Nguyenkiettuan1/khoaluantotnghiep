# SGU Vector Search System

Hệ thống tìm kiếm thông tin Đại học Sài Gòn sử dụng Vector Search và OpenAI

## Mục đích dự án | Project Purpose

### Tiếng Việt
Dự án này xây dựng một hệ thống tìm kiếm thông tin thông minh cho Trường Đại học Sài Gòn, sử dụng:
- Vector Search trong Neo4j để tìm kiếm ngữ nghĩa
- OpenAI để tạo vector embeddings và sinh câu trả lời
- Giao diện web thân thiện với người dùng

Hệ thống cho phép:
- Tìm kiếm thông tin về khoa, ngành đào tạo, học bổng, hợp tác quốc tế
- Trả lời câu hỏi dựa trên kết quả tìm kiếm
- Phân tích độ tin cậy của thông tin

### English
This project implements an intelligent information retrieval system for Saigon University, utilizing:
- Neo4j Vector Search for semantic search
- OpenAI for vector embeddings and answer generation
- User-friendly web interface

The system enables:
- Searching information about departments, programs, scholarships, international cooperation
- Answering questions based on search results
- Analyzing information reliability

## Kiến trúc hệ thống | System Architecture

```
┌─────────────┐    ┌──────────┐    ┌───────────┐
│   Streamlit │    │  Neo4j   │    │  OpenAI   │
│  Interface  │<-->│ Database │<-->│   API     │
└─────────────┘    └──────────┘    └───────────┘
```

- **Frontend**: Streamlit web interface
- **Backend**: Neo4j with vector search capability
- **AI Integration**: OpenAI for embeddings and answer generation
- **Data**: University information stored as graph data

## Cài đặt | Installation

1. Tạo môi trường ảo | Create virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/Mac
   ```

2. Cài đặt các gói phụ thuộc | Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Cấu hình môi trường | Configure environment:
   ```bash
   # Tạo file .env | Create .env file
   cp .env.example .env
   
   # Cập nhật thông tin trong .env | Update .env with your credentials
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your-password
   NEO4J_DATABASE=neo4j
   OPENAI_API_KEY=your-openai-key
   ```

## Chạy ứng dụng | Running the Application

1. Khởi động Neo4j | Start Neo4j:
   - Đảm bảo Neo4j Enterprise Edition đang chạy | Ensure Neo4j Enterprise Edition is running
   - Kiểm tra kết nối đến database | Verify database connection

2. Chạy ứng dụng web | Run web application:
   ```bash
   streamlit run app.py
   ```

## Sử dụng | Usage

1. Truy cập giao diện web | Access web interface:
   - Mở trình duyệt | Open browser
   - Truy cập | Navigate to: http://localhost:8501

2. Tìm kiếm thông tin | Search information:
   - Nhập câu hỏi | Enter your question
   - Chọn loại nội dung cần tìm | Select content types
   - Điều chỉnh các tham số tìm kiếm | Adjust search parameters

3. Xem kết quả | View results:
   - Câu trả lời được sinh tự động | Auto-generated answer
   - Kết quả tìm kiếm chi tiết | Detailed search results
   - Độ tin cậy của thông tin | Information reliability

## Lưu ý | Notes

- Hệ thống yêu cầu Neo4j Enterprise Edition để sử dụng Vector Search
- API key của OpenAI cần có đủ quota để xử lý embeddings và sinh câu trả lời
- Dữ liệu trong Neo4j cần được cập nhật thường xuyên để đảm bảo độ chính xác
- Log files được lưu trong thư mục `logs` với định dạng UTF-8

## Cấu trúc dự án | Project Structure

```
project/
├── app.py                 # Streamlit web interface
├── neo4jconnector.py      # Neo4j connection and vector search
├── requirements.txt       # Project dependencies
├── .env                   # Environment configuration
├── .env.example          # Environment template
└── logs/                 # Log files directory
```

## Hỗ trợ | Support

Nếu bạn gặp vấn đề hoặc cần hỗ trợ:
- Kiểm tra logs trong thư mục `logs`
- Đảm bảo các thông tin xác thực trong file `.env` chính xác
- Kiểm tra kết nối đến Neo4j và OpenAI

If you encounter issues or need support:
- Check logs in the `logs` directory
- Ensure credentials in `.env` are correct
- Verify connections to Neo4j and OpenAI
