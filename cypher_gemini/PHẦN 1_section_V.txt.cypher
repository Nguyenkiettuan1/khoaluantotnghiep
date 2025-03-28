cypher
MATCH (u:University {name: 'Trường Đại học Sài Gòn'})
WITH u
MERGE (r_sv_coban:Research {name: 'Đề tài Nghiên cứu khoa học sinh viên cấp cơ sở'})
ON CREATE SET r_sv_coban.description = 'Hoạt động nghiên cứu khoa học dành cho sinh viên Trường Đại học Sài Gòn, thực hiện trong 06-09 tháng dưới sự hướng dẫn của giảng viên. Điều kiện tham gia: kết quả học tập từ trung bình trở lên (khá cho chủ nhiệm), không bị kỷ luật, không có đề tài bị hủy/không đạt năm trước. Quyền lợi: hỗ trợ kinh phí, cộng điểm rèn luyện, cấp giấy chứng nhận, xét thưởng (Euréka, Bộ GD&ĐT, cấp trường), ưu tiên xét học bổng.'
ON MATCH SET r_sv_coban.description = 'Hoạt động nghiên cứu khoa học dành cho sinh viên Trường Đại học Sài Gòn, thực hiện trong 06-09 tháng dưới sự hướng dẫn của giảng viên. Điều kiện tham gia: kết quả học tập từ trung bình trở lên (khá cho chủ nhiệm), không bị kỷ luật, không có đề tài bị hủy/không đạt năm trước. Quyền lợi: hỗ trợ kinh phí, cộng điểm rèn luyện, cấp giấy chứng nhận, xét thưởng (Euréka, Bộ GD&ĐT, cấp trường), ưu tiên xét học bổng.'
MERGE (u)-[:conductsResearch]->(r_sv_coban)
WITH u
MERGE (s:Student {name: 'Sinh viên Đại học Sài Gòn'})
ON CREATE SET s.description = 'Toàn thể sinh viên đang theo học tại Trường Đại học Sài Gòn, có cơ hội tham gia các hoạt động nghiên cứu khoa học và nhận các hỗ trợ, quyền lợi liên quan.'
ON MATCH SET s.description = 'Toàn thể sinh viên đang theo học tại Trường Đại học Sài Gòn, có cơ hội tham gia các hoạt động nghiên cứu khoa học và nhận các hỗ trợ, quyền lợi liên quan.'
MERGE (u)-[:hasStudent]->(s)
WITH u
MERGE (f:Faculty {name: 'Giảng viên Đại học Sài Gòn'})
ON CREATE SET f.description = 'Đội ngũ giảng viên của Trường Đại học Sài Gòn, tham gia hướng dẫn sinh viên trong các hoạt động nghiên cứu khoa học.'
ON MATCH SET f.description = 'Đội ngũ giảng viên của Trường Đại học Sài Gòn, tham gia hướng dẫn sinh viên trong các hoạt động nghiên cứu khoa học.'
MERGE (u)-[:hasFaculty]->(f)
WITH u
MERGE (r_sv_xuatban:Research {name: 'Hoạt động xuất bản bài báo và báo cáo hội thảo của sinh viên'})
ON CREATE SET r_sv_xuatban.description = 'Hoạt động công bố kết quả nghiên cứu của sinh viên Trường Đại học Sài Gòn thông qua bài báo trên tạp chí chuyên ngành (trong nước, quốc tế) hoặc báo cáo tại hội thảo/hội nghị cấp quốc gia, quốc tế. Sản phẩm được công bố (tính điểm khoa học theo danh mục Hội đồng Giáo sư Nhà nước) nộp về Phòng Quản lý Khoa học sẽ được xét thưởng kinh phí và cộng điểm rèn luyện.'
ON MATCH SET r_sv_xuatban.description = 'Hoạt động công bố kết quả nghiên cứu của sinh viên Trường Đại học Sài Gòn thông qua bài báo trên tạp chí chuyên ngành (trong nước, quốc tế) hoặc báo cáo tại hội thảo/hội nghị cấp quốc gia, quốc tế. Sản phẩm được công bố (tính điểm khoa học theo danh mục Hội đồng Giáo sư Nhà nước) nộp về Phòng Quản lý Khoa học sẽ được xét thưởng kinh phí và cộng điểm rèn luyện.'
MERGE (u)-[:conductsResearch]->(r_sv_xuatban)
WITH u
MERGE (j:Journal {name: 'Tạp chí chuyên ngành và Kỷ yếu Hội thảo'})
ON CREATE SET j.description = 'Các ấn phẩm khoa học trong nước và quốc tế, bao gồm tạp chí chuyên ngành và kỷ yếu hội thảo/hội nghị, nơi sinh viên Trường Đại học Sài Gòn có thể công bố các bài báo và báo cáo khoa học của mình.'
ON MATCH SET j.description = 'Các ấn phẩm khoa học trong nước và quốc tế, bao gồm tạp chí chuyên ngành và kỷ yếu hội thảo/hội nghị, nơi sinh viên Trường Đại học Sài Gòn có thể công bố các bài báo và báo cáo khoa học của mình.'
MERGE (u)-[:publishesIn]->(j)
WITH u
MATCH (d_qlkh:Department {name: 'Phòng Quản lý khoa học'})
MERGE (r_qc_khcn:Research {name: 'Quy chế quản lý hoạt động Khoa học và Công nghệ'})
ON CREATE SET r_qc_khcn.description = 'Văn bản quy định về việc quản lý các hoạt động Khoa học và Công nghệ tại Trường Đại học Sài Gòn, bao gồm cả hoạt động nghiên cứu khoa học của sinh viên (chi tiết tại Chương 7). Phòng Quản lý Khoa học và Trợ lý NCKH của Khoa là đầu mối thông tin.'
ON MATCH SET r_qc_khcn.description = 'Văn bản quy định về việc quản lý các hoạt động Khoa học và Công nghệ tại Trường Đại học Sài Gòn, bao gồm cả hoạt động nghiên cứu khoa học của sinh viên (chi tiết tại Chương 7). Phòng Quản lý Khoa học và Trợ lý NCKH của Khoa là đầu mối thông tin.'
MERGE (u)-[:conductsResearch]->(r_qc_khcn)