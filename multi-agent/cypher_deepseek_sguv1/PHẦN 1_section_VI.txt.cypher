**Tạo các node và mối quan hệ cho thông tin về tạp chí khoa học:**

// Tạo node cho tạp chí khoa học
MERGE (journal:Journal {
  name: "Tạp chí Khoa học Đại học Sài Gòn",
  description: "Tạp chí khoa học công bố các kết quả nghiên cứu của trường Đại học Sài Gòn",
  publisher: "Trường Đại học Sài Gòn",
  address: "273 An Dương Vương, Phường 3, Quận 5, TP. Hồ Chí Minh",
  phone: "(028) 38 321 360",
  email: "tcdhsg@sgu.edu.vn",
  website: "http://sj.sgu.edu.vn/",
  license: "Số 22/GP-BTTTT",
  issn: "1859-3208"
})

// Tạo node cho trường Đại học Sài Gòn
MERGE (univ:University {
  name: "Trường Đại học Sài Gòn",
  description: "Trường đại học công lập tại TP. Hồ Chí Minh"
})

// Tạo mối quan hệ giữa trường và tạp chí
MERGE (univ)-[:PUBLISHES]->(journal)

// Tạo node cho quy định bài báo khoa học
MERGE (articleRegulation:Regulation {
  name: "Quy định bài báo khoa học",
  description: "Các yêu cầu và quy chuẩn cho bài báo đăng trên tạp chí"
})

// Tạo mối quan hệ giữa tạp chí và quy định
MERGE (journal)-[:HAS_REGULATION]->(articleRegulation)

// Tạo node cho tiêu chuẩn IEEE
MERGE (ieee:Standard {
  name: "Tiêu chuẩn IEEE",
  description: "Tiêu chuẩn trích dẫn cho bài báo khoa học tự nhiên"
})

// Tạo node cho tiêu chuẩn APA
MERGE (apa:Standard {
  name: "Tiêu chuẩn APA",
  description: "Tiêu chuẩn trích dẫn cho bài báo khoa học xã hội"
})

// Tạo mối quan hệ giữa quy định và các tiêu chuẩn
MERGE (articleRegulation)-[:USES_STANDARD]->(ieee)
MERGE (articleRegulation)-[:USES_STANDARD]->(apa)

// Tạo node cho yêu cầu bài báo
MERGE (articleRequirement:Requirement {
  name: "Yêu cầu bài báo",
  description: "Các yêu cầu kỹ thuật cho bài báo khoa học"
})

// Tạo mối quan hệ giữa quy định và yêu cầu
MERGE (articleRegulation)-[:HAS_REQUIREMENT]->(articleRequirement)

// Tạo node cho quy trình gửi bài
MERGE (submissionProcess:Process {
  name: "Quy trình gửi bài",
  description: "Quy trình gửi bài báo khoa học"
})

// Tạo mối quan hệ giữa tạp chí và quy trình
MERGE (journal)-[:HAS_PROCESS]->(submissionProcess)

// Tạo node cho ban biên tập
MERGE (editorialBoard:Organization {
  name: "Ban biên tập Tạp chí Khoa học Đại học Sài Gòn",
  description: "Ban phụ trách biên tập nội dung tạp chí"
})

// Tạo mối quan hệ giữa tạp chí và ban biên tập
MERGE (journal)-[:HAS_EDITORIAL_BOARD]->(editorialBoard)