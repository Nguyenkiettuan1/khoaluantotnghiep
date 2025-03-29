
MERGE (u:University {name: "Trường Đại học Sài Gòn", description: "Trường Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, đào tạo đa ngành từ trình độ đại học đến sau đại học với các phương thức chính quy và giáo dục thường xuyên"})

MERGE (j:Journal {
  name: "Tạp chí Khoa học Đại học Sài Gòn",
  description: "Tạp chí khoa học công bố kết quả nghiên cứu của cán bộ, giảng viên trường Đại học Sài Gòn, diễn đàn trao đổi kinh nghiệm giảng dạy và học tập",
  fullName: "Scientific Journal of Saigon University",
  address: "273 An Dương Vương, Phường 3, Quận 5, TP. Hồ Chí Minh",
  phone: "(028) 38 321 360",
  email: "tcdhsg@sgu.edu.vn",
  website: "http://sj.sgu.edu.vn/",
  license: "Số 22/GP-BTTTT do Bộ Thông tin và Truyền thông cấp ngày 23/01/2015",
  issn: "1859-3208",
  impactScore: "20 điểm theo Hội đồng Chức danh Giáo sư Nhà nước"
})

MERGE (j)-[:publishedBy]->(u)

MERGE (a1:ArticleRequirement {
  name: "Yêu cầu nội dung bài báo",
  description: "Phải nêu rõ mục tiêu nghiên cứu, có kết quả mới, giá trị khoa học và thực tiễn, được phản biện, có chú thích và tài liệu tham khảo"
})

MERGE (a2:ArticleRequirement {
  name: "Yêu cầu hình thức bài báo",
  description: "Không quá 12 trang A4 (4000-5000 từ), font Times New Roman 13, giãn dòng 1.5, lề trên 25mm/dưới 20mm/trái 30mm/phải 20mm"
})

MERGE (a3:ArticleRequirement {
  name: "Cấu trúc bài báo",
  description: "Gồm tiêu đề Việt-Anh, tác giả, tóm tắt, từ khóa, nội dung (mở đầu, nội dung chính, kết luận), chú thích, tài liệu tham khảo"
})

MERGE (a4:ArticleRequirement {
  name: "Trích dẫn tài liệu",
  description: "Theo tiêu chuẩn IEEE (Khoa học Tự nhiên) hoặc APA (Khoa học Xã hội và Giáo dục)"
})

MERGE (a5:ArticleRequirement {
  name: "Hình ảnh minh họa",
  description: "Độ phân giải 300dpi trở lên, định dạng vector (EPS, PDF, AI) hoặc ảnh (PNG, JPG, BMP)"
})

MERGE (d:Department {
  name: "Ban Biên tập Tạp chí Khoa học",
  description: "Phụ trách biên tập và xuất bản Tạp chí Khoa học Đại học Sài Gòn",
  location: "Phòng C010, 273 An Dương Vương, Q.5, TP.HCM"
})

MERGE (j)-[:hasRequirement]->(a1)
MERGE (j)-[:hasRequirement]->(a2)
MERGE (j)-[:hasRequirement]->(a3)
MERGE (j)-[:hasRequirement]->(a4)
MERGE (j)-[:hasRequirement]->(a5)
MERGE (j)-[:managedBy]->(d)
MERGE (d)-[:partOf]->(u)

MERGE (s1:SubmissionProcess {
  name: "Quy trình gửi bài",
  description: "Gửi bài qua email tcdhsg@sgu.edu.vn hoặc nộp trực tiếp tại tòa soạn"
})

MERGE (s2:SubmissionProcess {
  name: "Yêu cầu bài gửi",
  description: "Công trình khoa học mới, chưa công bố, có giá trị khoa học và thực tiễn, viết bằng tiếng Việt hoặc tiếng Anh"
})

MERGE (j)-[:hasSubmissionProcess]->(s1)
MERGE (j)-[:hasSubmissionProcess]->(s2)