MERGE (u:University {name: "Trường Đại học Sài Gòn", description: "Trường đại học công lập đa ngành, đa lĩnh vực trực thuộc UBND TP. Hồ Chí Minh"})

MERGE (org1:Organization {name: "Bộ Khoa học và Công nghệ", description: "Cơ quan quản lý nhà nước về khoa học và công nghệ tại Việt Nam"})
MERGE (org2:Organization {name: "Bộ Giáo dục và Đào tạo", description: "Cơ quan quản lý nhà nước về giáo dục tại Việt Nam"})
MERGE (u)-[:hasManagement]->(org1)
MERGE (u)-[:hasManagement]->(org2)

MERGE (int1:InternationalCooperation {name: "Đại học Khoa học Ứng dụng IMC Krems", description: "Trường đại học tại Cộng hòa Áo, đối tác liên kết đào tạo với Đại học Sài Gòn"})
MERGE (int2:InternationalCooperation {name: "Hiệp hội Phát triển Kinh tế Văn hóa Giáo dục Đài Việt", description: "Tổ chức hợp tác giáo dục giữa Đài Loan và Việt Nam"})
MERGE (int3:InternationalCooperation {name: "Bộ Y tế Singapore", description: "Cơ quan quản lý y tế tại Singapore, cung cấp học bổng Asian Nursing Scholarship"})
MERGE (int4:InternationalCooperation {name: "Đại học Huddersfield", description: "Trường đại học tại Vương quốc Anh, đối tác liên kết đào tạo với Đại học Sài Gòn"})
MERGE (u)-[:hasInternationalCooperations]->(int1)
MERGE (u)-[:hasInternationalCooperations]->(int2)
MERGE (u)-[:hasInternationalCooperations]->(int3)
MERGE (u)-[:hasInternationalCooperations]->(int4)

MERGE (prog1:Program {name: "Cử nhân Quốc tế Quản trị Kinh doanh và Quản lý Thương mại Điện tử", description: "Chương trình liên kết với Đại học Khoa học Ứng dụng IMC Krems (Áo)"})
MERGE (deg1:Degree {name: "Cử nhân Quản trị Kinh doanh và Quản lý Thương mại Điện tử", description: "Bằng cấp quốc tế được cấp bởi Đại học Khoa học Ứng dụng IMC Krems"})
MERGE (prog1)-[:hasDegree]->(deg1)
MERGE (u)-[:offersPrograms]->(prog1)

MERGE (prog2:Program {name: "Đào tạo tiếng Hoa", description: "Chương trình liên kết với Hiệp hội Phát triển Kinh tế Văn hóa Giáo dục Đài Việt"})
MERGE (deg2:Degree {name: "Chứng chỉ Hoa ngữ", description: "Chứng chỉ tiếng Hoa được cấp bởi Trung tâm Hoa Ngữ Sư Phạm Đài Loan"})
MERGE (prog2)-[:hasDegree]->(deg2)
MERGE (u)-[:offersPrograms]->(prog2)

MERGE (sch1:Scholarship {name: "Asian Nursing Scholarship", description: "Học bổng toàn phần đào tạo Trợ lý bác sĩ tại Singapore với trị giá SGD 120,000"})
MERGE (u)-[:awardedScholarships]->(sch1)

MERGE (prog3:Program {name: "Thạc sĩ Giảng dạy tiếng Anh (TESOL)", description: "Chương trình liên kết với Đại học Huddersfield (Anh)"})
MERGE (deg3:Degree {name: "Thạc sĩ TESOL", description: "Bằng thạc sĩ giảng dạy tiếng Anh được cấp bởi Đại học Huddersfield"})
MERGE (prog3)-[:hasDegree]->(deg3)
MERGE (u)-[:offersPrograms]->(prog3)

MERGE (dept1:Department {name: "Phòng Hợp tác quốc tế", description: "Đơn vị quản lý các hoạt động hợp tác quốc tế của trường"})
MERGE (u)-[:hasDepartments]->(dept1)