# ChatRule Pipeline cho Neo4j Knowledge Graph

Pipeline này triển khai phương pháp ChatRule để khai thác các quy tắc logic từ Knowledge Graph (KG) được lưu trữ trong Neo4j, kết hợp với Language Model (LLM).

## Cấu trúc

Pipeline gồm 3 thành phần chính:

1. **RuleSampler**: Lấy mẫu và tạo rules từ KG
   - Lấy mẫu ngẫu nhiên các cặp node được kết nối bởi relation đích
   - Tìm các đường đi thay thế không sử dụng relation đích
   - Chuyển đổi đường đi thành rules logic

2. **LLMRuleGenerator**: Sinh rules mới sử dụng LLM
   - Sử dụng rules mẫu làm few-shot examples
   - Tạo prompt thông minh cho LLM
   - Parse kết quả từ LLM thành rules

3. **RuleRanker**: Đánh giá và xếp hạng rules
   - Tính toán các metrics: support, coverage, confidence, PCA-confidence
   - Lọc rules dựa trên ngưỡng support tối thiểu
   - Xếp hạng rules theo PCA-confidence

## Cài đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install neo4j openai python-dotenv
```

2. Tạo file `.env` với các thông tin cấu hình:
```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j
OPENAI_API_KEY=your_openai_api_key
```

## Sử dụng

1. Import và khởi tạo pipeline:
```python
from neo4jconnector import Neo4jConnection
from chatrule import ChatRulePipeline

neo4j = Neo4jConnection(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password",
    dbname="neo4j"
)

pipeline = ChatRulePipeline(neo4j)
```

2. Chạy pipeline cho một relation cụ thể:
```python
results = pipeline.run(target_relation="HAS_PREREQUISITE")
```

3. Hoặc chạy cho tất cả relations trong KG:
```python
results = pipeline.run()
```

4. Lưu kết quả:
```python
pipeline.save_results(results, "chatrule_results.txt")
```

## Format Rules

Rules được biểu diễn theo cú pháp Datalog/Prolog:
```
head(X, Y) :- relation1(X, Z1), relation2(Z1, Z2), relation3(Z2, Y)
```

Ví dụ:
```
HAS_PREREQUISITE(X, Y) :- PART_OF(X, Z), HAS_PREREQUISITE(Z, Y)
```

## Metrics

1. **Support**: Số lượng cặp entities thỏa mãn cả head và body của rule
2. **Coverage**: Support / Tổng số triples có relation head
3. **Confidence**: Support / Số lượng triples thỏa mãn body
4. **PCA-Confidence**: (Confidence + Coverage) / 2

## Tùy chỉnh

Các tham số có thể điều chỉnh:
- `max_path_length`: Độ dài tối đa của đường đi (mặc định: 3)
- `samples_per_relation`: Số lượng mẫu cho mỗi relation (mặc định: 5)
- `num_examples`: Số lượng ví dụ few-shot cho LLM (mặc định: 3)
- `num_generated`: Số lượng rules mới sinh bởi LLM (mặc định: 5)
- `min_support`: Ngưỡng support tối thiểu (mặc định: 1)

## Lưu ý

1. Đảm bảo KG trong Neo4j có đủ dữ liệu và kết nối phù hợp
2. Rules sinh ra bởi LLM cần được kiểm tra về tính hợp lệ
3. Điều chỉnh các tham số tùy theo kích thước và đặc điểm của KG
4. Nên chạy thử nghiệm trên tập con của KG trước khi chạy toàn bộ
5. Monitor usage của OpenAI API để kiểm soát chi phí

## Khắc phục sự cố

1. **Lỗi kết nối Neo4j**:
   - Kiểm tra thông tin đăng nhập
   - Đảm bảo Neo4j server đang chạy
   - Kiểm tra firewall settings

2. **Lỗi OpenAI API**:
   - Verify API key
   - Kiểm tra quota và billing
   - Xử lý rate limiting

3. **Memory Issues**:
   - Giảm `samples_per_relation`
   - Giảm `max_path_length`
   - Chạy từng relation một thay vì tất cả

## Liên hệ hỗ trợ

Nếu gặp vấn đề hoặc cần hỗ trợ, vui lòng tạo issue trên repository hoặc liên hệ trực tiếp.