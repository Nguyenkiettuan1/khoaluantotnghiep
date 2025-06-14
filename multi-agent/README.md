# Multi-Agent Ontology Generation System

Hệ thống tạo ontology tự động sử dụng nhiều mô hình AI để xây dựng knowledge graph từ dữ liệu văn bản.

## Tính năng chính

- 🤖 **Multi-Agent**: Sử dụng đồng thời 3 mô hình AI (OpenAI GPT, Google Gemini, DeepSeek)
- 📋 **Tự động tạo CQs**: Sinh câu hỏi năng lực từ dữ liệu đầu vào
- 🔗 **Skeleton Ontology**: Tạo ontology cơ bản từ competency questions
- ⚡ **Xử lý song song**: Tối ưu hiệu suất với async/await
- 💾 **Neo4j Integration**: Tự động import vào nhiều database Neo4j
- 📊 **Vector Search**: Hỗ trợ tìm kiếm similarity với OpenAI embeddings

## Cấu trúc thư mục

```
multi-agent/
├── main.py                          # Script chính điều phối workflow
├── generate_cqs.py                  # Tạo competency questions
├── generate_skeleton_ontology.py    # Tạo ontology cơ bản
├── generate_ontology_parallel.py    # Tạo Cypher với nhiều models
├── import_to_neo4j.py              # Import dữ liệu vào Neo4j
├── neo4jconnector.py               # Kết nối và xử lý Neo4j
├── utils.py                        # Các hàm tiện ích
├── model_configs.py                # Cấu hình các AI models
├── gemini_config.py                # Cấu hình Gemini
├── prompts/                        # Các template prompts
│   ├── prompts_cypher.yaml
│   └── prompts_cq.yaml
├── dataset/                        # Dữ liệu đầu vào
├── CQs/                           # Competency Questions
├── ontology/                      # Ontology files
├── cypher_deepseek_sguv1/         # Cypher từ DeepSeek
├── cypher_gemini_sguv2/           # Cypher từ Gemini
├── cypher_openai_sguv3/           # Cypher từ OpenAI
└── logs/                          # Log files
```

## Cài đặt

### 1. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 2. Cấu hình environment variables

Sao chép file `.env.example` thành `.env` và điền các API keys:

```bash
cp .env.example .env
```

Chỉnh sửa file `.env`:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key

# OpenRouter Configuration (for DeepSeek)
OPENROUTER_API_KEY=sk-or-your-openrouter-key

# Google Gemini Configuration  
GOOGLE_API_KEY=your-google-ai-key

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
NEO4J_DATABASE=neo4j
```

### 3. Chuẩn bị dữ liệu

Đặt các file dữ liệu (.txt) vào thư mục `dataset/`

## Sử dụng

### Chạy workflow hoàn chỉnh

```bash
python main.py --complete
```

### Chạy từng bước riêng lẻ

```bash
# Bước 1: Tạo competency questions
python main.py --step 1 --questions 50

# Bước 2: Tạo skeleton ontology
python main.py --step 2

# Bước 3: Tạo Cypher với multi-agents
python main.py --step 3

# Bước 4: Import vào Neo4j
python main.py --step 4
```

### Bỏ qua một số bước

```bash
# Chạy workflow nhưng bỏ qua bước 1 và 2
python main.py --complete --skip 1 2
```

## Workflow

1. **Generate Competency Questions**: Tạo câu hỏi năng lực từ dataset
2. **Generate Skeleton Ontology**: Tạo ontology cơ bản từ CQs
3. **Generate Cypher (Multi-Agent)**: 3 AI models song song tạo Cypher
4. **Import to Neo4j**: Import vào 3 database riêng biệt

## Các Models được hỗ trợ

- **OpenAI GPT-4o-mini**: Mô hình chính xác, ổn định
- **Google Gemini**: Hiệu suất cao, xử lý context dài
- **DeepSeek**: Mô hình mã nguồn mở, hiệu quả về chi phí

## Monitoring & Logs

Logs được lưu trong thư mục `logs/` với format:
- `main_YYYYMMDD_HHMMSS.log`: Log workflow chính
- `neo4j_vector_search_YYYYMMDD.log`: Log Neo4j operations

## Troubleshooting

### Lỗi API Keys
- Kiểm tra file `.env` đã được cấu hình đúng
- Verify API keys còn hạn và có đủ credits

### Lỗi Neo4j Connection
- Đảm bảo Neo4j server đang chạy
- Kiểm tra URI, username, password trong `.env`
- Verify database names tồn tại

### Lỗi Memory
- Giảm batch size trong `chunk_text()`
- Increase timeout cho các API calls
- Monitor system resources

## Customization

### Thêm Model mới

1. Tạo class trong `model_configs.py`
2. Extend `ModelConfig` trong `generate_ontology_parallel.py`
3. Thêm vào list `models` trong `main()`

### Tùy chỉnh Prompts

Chỉnh sửa các file YAML trong thư mục `prompts/`:
- `prompts_cypher.yaml`: Template cho việc tạo Cypher
- `prompts_cq.yaml`: Template cho việc tạo competency questions

## Dependencies

Xem file `requirements.txt` để biết chi tiết về các dependencies cần thiết.

## License

[Thêm thông tin license nếu cần]
