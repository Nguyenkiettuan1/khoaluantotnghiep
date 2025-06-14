**Tạo các node và mối quan hệ cho thông tin về nghiên cứu khoa học sinh viên:**


// Tạo node cho chương trình NCKH sinh viên
MERGE (program:Program {
  name: "Nghiên cứu khoa học sinh viên",
  description: "Chương trình nghiên cứu khoa học dành cho sinh viên với các đề tài cấp cơ sở"
})

// Tạo node cho quy định tham gia NCKH
MERGE (regulation:Regulation {
  name: "Quy định NCKH sinh viên",
  description: "Các điều kiện và quy định tham gia nghiên cứu khoa học cho sinh viên"
})

// Tạo node cho giải thưởng NCKH
MERGE (award:Award {
  name: "Giải thưởng NCKH sinh viên",
  description: "Các giải thưởng dành cho sinh viên có thành tích xuất sắc trong nghiên cứu khoa học"
})

// Tạo mối quan hệ giữa chương trình và quy định
MERGE (program)-[:HAS_REGULATION]->(regulation)

// Tạo mối quan hệ giữa chương trình và giải thưởng
MERGE (program)-[:HAS_AWARD]->(award)

// Tạo node cho bài báo khoa học
MERGE (journal:Journal {
  name: "Bài báo khoa học sinh viên",
  description: "Các bài báo khoa học được công bố bởi sinh viên"
})

// Tạo mối quan hệ giữa chương trình và bài báo
MERGE (program)-[:HAS_PUBLICATION]->(journal)

// Tạo node cho hội thảo khoa học
MERGE (conference:Conference {
  name: "Hội thảo khoa học sinh viên",
  description: "Các hội thảo khoa học cấp quốc gia và quốc tế"
})

// Tạo mối quan hệ giữa chương trình và hội thảo
MERGE (program)-[:HAS_CONFERENCE]->(conference)


**Tạo các node và mối quan hệ cho thông tin về giải thưởng:**


// Tạo node cho giải thưởng EURÉKA
MERGE (eureka:Award {
  name: "Giải thưởng EURÉKA",
  description: "Giải thưởng nghiên cứu khoa học do Thành đoàn TP.HCM tổ chức"
})

// Tạo node cho giải thưởng Bộ GD&ĐT
MERGE (moet:Award {
  name: "Giải thưởng Bộ Giáo dục và Đào tạo",
  description: "Giải thưởng nghiên cứu khoa học do Bộ GD&ĐT tổ chức"
})

// Tạo mối quan hệ giữa chương trình và các giải thưởng
MERGE (program)-[:HAS_AWARD]->(eureka)
MERGE (program)-[:HAS_AWARD]->(moet)


**Tạo mối quan hệ với trường đại học:**


// Giả sử đã có node trường đại học
MATCH (u:University {name: "Trường Đại học Sài Gòn"})

// Tạo mối quan hệ giữa trường và chương trình NCKH
MERGE (u)-[:HAS_PROGRAM]->(program)


**Tạo node cho quy chế NCKH:**


MERGE (regulationDoc:Document {
  name: "Quy chế quản lý hoạt động Khoa học và Công nghệ",
  description: "Quy định chính thức về hoạt động nghiên cứu khoa học tại trường"
})

// Tạo mối quan hệ giữa quy định và tài liệu
MERGE (regulation)-[:HAS_DOCUMENT]->(regulationDoc)