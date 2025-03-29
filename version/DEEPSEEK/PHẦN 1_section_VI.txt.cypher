MERGE (university:Truong_Dai_hoc {name: "Trường Đại học Sài Gòn", description: "Trường Đại học Sài Gòn là cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh"})

// Tạp chí Khoa học
MERGE (journal:Tap_chi {name: "Tạp chí Khoa học Đại học Sài Gòn", 
description: "Tạp chí khoa học công bố kết quả nghiên cứu của cán bộ, giảng viên trường Đại học Sài Gòn. ISSN: 1859-3208, được Hội đồng Chức danh Giáo sư Nhà nước công nhận tính điểm 20 ngành khoa học",
address: "273 An Dương Vương, Phường 3, Quận 5, TP. Hồ Chí Minh",
phone: "(028) 38 321 360",
email: "tcdhsg@sgu.edu.vn",
website: "http://sj.sgu.edu.vn/",
license: "Số 22/GP-BTTTT do Bộ Thông tin và Truyền thông cấp ngày 23/01/2015",
issn: "1859-3208"})

// Mục đích tạp chí
MERGE (purpose1:Muc_dich {name: "Diễn đàn khoa học", description: "Công bố kết quả nghiên cứu và hoạt động khoa học của cán bộ, giảng viên"})
MERGE (purpose2:Muc_dich {name: "Trao đổi kinh nghiệm", description: "Diễn đàn trao đổi kinh nghiệm giảng dạy, học tập của giáo viên và sinh viên"})
MERGE (purpose3:Muc_dich {name: "Cầu nối giáo dục", description: "Kết nối giữa trường Đại học Sài Gòn với các cơ sở giáo dục khác"})
MERGE (purpose4:Muc_dich {name: "Gắn kết nghiên cứu - thực tiễn", description: "Cầu nối giữa nghiên cứu với thực tiễn đời sống kinh tế - xã hội"})

// Yêu cầu bài báo
MERGE (requirement1:Yeu_cau {name: "Nội dung khoa học", description: "Phải có kết quả mới, giá trị khoa học và thực tiễn, được phản biện"})
MERGE (requirement2:Yeu_cau {name: "Cấu trúc bài báo", description: "Gồm mục tiêu, đối tượng nghiên cứu, giải quyết vấn đề và kết luận"})
MERGE (requirement3:Yeu_cau {name: "Trích dẫn rõ ràng", description: "Chú rõ nguồn khi trích dẫn, sử dụng kết quả nghiên cứu khác"})
MERGE (requirement4:Yeu_cau {name: "Đa ngôn ngữ", description: "Có tiêu đề, tóm tắt, từ khóa bằng tiếng Việt và tiếng Anh"})

// Quy định trình bày
MERGE (format1:Quy_dinh {name: "Độ dài bài báo", description: "Không quá 12 trang A4 (4000-5000 từ)"})
MERGE (format2:Quy_dinh {name: "Định dạng văn bản", description: "Soạn thảo Word, Unicode, Font Times New Roman 13, giãn dòng 1.5"})
MERGE (format3:Quy_dinh {name: "Công thức toán học", description: "Dùng MathType hoặc MS Equation, bài Toán/Vật lý có thể dùng LaTeX"})
MERGE (format4:Quy_dinh {name: "Hình ảnh minh họa", description: "Độ phân giải 300dpi trở lên, định dạng vector hoặc ảnh chất lượng cao"})

// Tiêu chuẩn trích dẫn
MERGE (citation1:Tieu_chuan {name: "IEEE", description: "Tiêu chuẩn trích dẫn cho lĩnh vực Khoa học Tự nhiên"})
MERGE (citation2:Tieu_chuan {name: "APA", description: "Tiêu chuẩn trích dẫn cho lĩnh vực Khoa học Xã hội và Giáo dục"})

// Đối tượng độc giả
MERGE (reader1:Doi_tuong {name: "Giảng viên đại học", description: "Cán bộ giảng dạy tại các trường đại học"})
MERGE (reader2:Doi_tuong {name: "Nhà nghiên cứu", description: "Các nhà nghiên cứu tại viện, trung tâm nghiên cứu"})
MERGE (reader3:Doi_tuong {name: "Sinh viên", description: "Sinh viên các trường đại học, cao đẳng"})
MERGE (reader4:Doi_tuong {name: "Nhà quản lý giáo dục", description: "Cán bộ quản lý trong lĩnh vực giáo dục"})

// Tạo quan hệ
MERGE (university)-[:publishes]->(journal)

// Quan hệ mục đích
MERGE (journal)-[:has_purpose]->(purpose1)
MERGE (journal)-[:has_purpose]->(purpose2)
MERGE (journal)-[:has_purpose]->(purpose3)
MERGE (journal)-[:has_purpose]->(purpose4)

// Quan hệ yêu cầu
MERGE (journal)-[:has_requirement]->(requirement1)
MERGE (journal)-[:has_requirement]->(requirement2)
MERGE (journal)-[:has_requirement]->(requirement3)
MERGE (journal)-[:has_requirement]->(requirement4)

// Quan hệ định dạng
MERGE (journal)-[:has_format]->(format1)
MERGE (journal)-[:has_format]->(format2)
MERGE (journal)-[:has_format]->(format3)
MERGE (journal)-[:has_format]->(format4)

// Quan hệ tiêu chuẩn trích dẫn
MERGE (journal)-[:uses_citation_standard]->(citation1)
MERGE (journal)-[:uses_citation_standard]->(citation2)

// Quan hệ đối tượng độc giả
MERGE (journal)-[:serves_audience]->(reader1)
MERGE (journal)-[:serves_audience]->(reader2)
MERGE (journal)-[:serves_audience]->(reader3)
MERGE (journal)-[:serves_audience]->(reader4)