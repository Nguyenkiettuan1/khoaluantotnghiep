MERGE (u:University {name: "Trường Đại học Sài Gòn", description: "Trường Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, đào tạo đa ngành từ trình độ đại học đến sau đại học với các phương thức chính quy và giáo dục thường xuyên"})

MERGE (org:Organization {name: "UBND TP. Hồ Chí Minh", description: "Ủy ban nhân dân Thành phố Hồ Chí Minh, cơ quan quản lý trực tiếp của Trường Đại học Sài Gòn"})
MERGE (u)-[:hasManagement]->(org)

MERGE (award:Award {name: "Huân chương Lao động Hạng Ba", description: "Giải thưởng do Chủ tịch nước Cộng hòa Xã hội Chủ nghĩa Việt Nam trao tặng năm 2018"})
MERGE (u)-[:hasAwards]->(award)

MERGE (cert:Degree {name: "Chứng chỉ Bồi dưỡng nghiệp vụ sư phạm", description: "Chứng chỉ đào tạo cho giảng viên đại học, cao đẳng và giáo viên Tiếng Anh Tiểu học"})
MERGE (u)-[:offersPrograms]->(:Program {name: "Bồi dưỡng nghiệp vụ sư phạm", description: "Chương trình đào tạo cấp chứng chỉ nghiệp vụ sư phạm"})-[:hasDegree]->(cert)

MERGE (itCert:Degree {name: "Chứng chỉ Công nghệ Thông tin", description: "Chứng chỉ đào tạo về Công nghệ Thông tin"})
MERGE (u)-[:offersPrograms]->(:Program {name: "Đào tạo Công nghệ Thông tin", description: "Chương trình đào tạo cấp chứng chỉ Công nghệ Thông tin"})-[:hasDegree]->(itCert)

MERGE (engCert:Degree {name: "Chứng chỉ Tiếng Anh theo khung năng lực Ngoại ngữ 6 bậc", description: "Chứng chỉ Tiếng Anh theo chuẩn quốc gia Việt Nam"})
MERGE (u)-[:offersPrograms]->(:Program {name: "Đào tạo Tiếng Anh", description: "Chương trình đào tạo cấp chứng chỉ Tiếng Anh theo khung 6 bậc"})-[:hasDegree]->(engCert)

MERGE (phd:Degree {name: "Tiến sĩ", description: "Bằng tiến sĩ với 5 chuyên ngành đào tạo"})
MERGE (u)-[:offersPrograms]->(:Program {name: "Đào tạo Tiến sĩ", description: "Chương trình đào tạo trình độ tiến sĩ với 5 chuyên ngành"})-[:hasDegree]->(phd)

MERGE (master:Degree {name: "Thạc sĩ", description: "Bằng thạc sĩ với 12 chuyên ngành đào tạo"})
MERGE (u)-[:offersPrograms]->(:Program {name: "Đào tạo Thạc sĩ", description: "Chương trình đào tạo trình độ thạc sĩ với 12 chuyên ngành"})-[:hasDegree]->(master)

MERGE (bachelor:Degree {name: "Cử nhân", description: "Bằng cử nhân với 39 chương trình đào tạo"})
MERGE (u)-[:offersPrograms]->(:Program {name: "Đào tạo Đại học", description: "Chương trình đào tạo trình độ đại học với 39 ngành thuộc các lĩnh vực Kinh tế, Kỹ thuật, Công nghệ, Văn hóa xã hội, Chính trị, Nghệ thuật và Sư phạm"})-[:hasDegree]->(bachelor)

MERGE (dept1:Department {name: "Khoa Kinh tế - Kỹ thuật - Công nghệ", description: "Khoa đào tạo các ngành thuộc lĩnh vực kinh tế, kỹ thuật và công nghệ"})
MERGE (dept2:Department {name: "Khoa Văn hóa xã hội", description: "Khoa đào tạo các ngành thuộc lĩnh vực văn hóa xã hội"})
MERGE (dept3:Department {name: "Khoa Chính trị", description: "Khoa đào tạo các ngành thuộc lĩnh vực chính trị"})
MERGE (dept4:Department {name: "Khoa Nghệ thuật", description: "Khoa đào tạo các ngành thuộc lĩnh vực nghệ thuật"})
MERGE (dept5:Department {name: "Khoa Sư phạm", description: "Khoa đào tạo các ngành thuộc lĩnh vực sư phạm"})
MERGE (u)-[:hasDepartments]->(dept1)
MERGE (u)-[:hasDepartments]->(dept2)
MERGE (u)-[:hasDepartments]->(dept3)
MERGE (u)-[:hasDepartments]->(dept4)
MERGE (u)-[:hasDepartments]->(dept5)

MERGE (research:Research {name: "Kiểm định chất lượng giáo dục", description: "Hoạt động nghiên cứu và đánh giá chất lượng giáo dục đại học"})
MERGE (u)-[:hasResearchProjects]->(research)

MERGE (journal:Journal {name: "Tạp chí Khoa học Đại học Sài Gòn", description: "Tạp chí khoa học do Trường Đại học Sài Gòn xuất bản"})
MERGE (journal)-[:publishesIn]->(u)
MERGE (journal)-[:hasArticles]->(research)