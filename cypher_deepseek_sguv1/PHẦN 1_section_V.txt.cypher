MERGE (u:University {name: "Trường Đại học Sài Gòn", description: "Trường Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, đào tạo đa ngành từ trình độ đại học đến sau đại học với các phương thức chính quy và giáo dục thường xuyên"})

// Nghiên cu khoa học sinh viên
MERGE (r1:ResearchPolicy {name: "Đề tài NCKH cấp cơ sở", description: "Sinh viên thực hiện đề tài trong 6-9 tháng dưới sự hướng dẫn của giảng viên, theo Quy chế quản lý hoạt động Khoa học và Công nghệ của Trường"})
MERGE (r2:ResearchPolicy {name: "Điều kiện tham gia NCKH", description: "SV phải có kết quả học tập trung bình trở lên, không bị k luật, không có đề tài bị hy/nghiệm thu không đạt năm trước"})
MERGE (r3:ResearchPolicy {name: "Quyền li NCKH", description: "Được h tr kinh phí, cộng điểm rèn luyện, cấp giấy chứng nhận; đề tài tốt/xuất sắc được thưng, dự thi giải thưng EURÉKA, SV NCKH cấp Bộ"})
MERGE (r4:ResearchPolicy {name: "Bài báo khoa học", description: "SV có bài báo đăng tạp chí chuyên ngành hoặc báo cáo hội thảo cấp quốc gia/quốc tế được xét thưng và cộng điểm rèn luyện"})

// Giải thưng nghiên cu khoa học
MERGE (a1:Award {name: "Giải thưng Sinh viên NCKH EURÉKA", description: "Giải thưng do Thành Đoàn TP.HCM t chức cho các đề tài NCKH xuất sắc"})
MERGE (a2:Award {name: "Giải thưng Sinh viên NCKH cấp Bộ", description: "Giải thưng do Bộ GD&ĐT t chức cho các đề tài NCKH xuất sắc"})
MERGE (a3:Award {name: "Giải thưng Sinh viên NCKH cấp cơ sở", description: "Giải thưng do Trường Đại học Sài Gòn t chức cho các đề tài NCKH xuất sắc"})

// Các phòng ban liên quan
MERGE (d1:Department {name: "Phòng Quản lý Khoa học", description: "Phụ trách quản lý hoạt động nghiên cu khoa học của trường, tiếp nhận và xét duyệt các đề tài NCKH"})
MERGE (d2:Department {name: "Tr lý nghiên cu khoa học", description: "Giảng viên phụ trách h tr hoạt động NCKH tại các khoa"})

// Tạo quan hệ với trường
WITH u, r1, r2, r3, r4, a1, a2, a3, d1, d2
MERGE (u)-[:hasResearchPolicy]->(r1)
MERGE (u)-[:hasResearchPolicy]->(r2)
MERGE (u)-[:hasResearchPolicy]->(r3)
MERGE (u)-[:hasResearchPolicy]->(r4)
MERGE (u)-[:hasAward]->(a1)
MERGE (u)-[:hasAward]->(a2)
MERGE (u)-[:hasAward]->(a3)
MERGE (u)-[:hasDepartment]->(d1)
MERGE (u)-[:hasDepartment]->(d2)

// Tạo quan hệ giữa các chính sách và giải thưng
MERGE (r1)-[:leadsTo]->(a1)
MERGE (r1)-[:leadsTo]->(a2)
MERGE (r1)-[:leadsTo]->(a3)
MERGE (r3)-[:includes]->(a1)
MERGE (r3)-[:includes]->(a2)
MERGE (r3)-[:includes]->(a3)
MERGE (d1)-[:manages]->(r1)
MERGE (d1)-[:manages]->(r2)
MERGE (d1)-[:manages]->(r3)
MERGE (d1)-[:manages]->(r4)