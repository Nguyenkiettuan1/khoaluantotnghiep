cypher
MERGE (u:University {name: 'Trường Đại học Sài Gòn'})
ON CREATE SET u.description = 'Cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo. Là trường đại học đào tạo đa ngành, đa lĩnh vực từ trình độ đại học và sau đại học theo phương thức chính quy và giáo dục thường xuyên. Được Chứng nhận kiểm định chất lượng giáo dục ngày 13/5/2017 và nhận Huân chương Lao động Hạng Ba năm 2018.'
ON MATCH SET u.description = 'Cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo. Là trường đại học đào tạo đa ngành, đa lĩnh vực từ trình độ đại học và sau đại học theo phương thức chính quy và giáo dục thường xuyên. Được Chứng nhận kiểm định chất lượng giáo dục ngày 13/5/2017 và nhận Huân chương Lao động Hạng Ba năm 2018.'
WITH u
MERGE (d1:Degree {name: 'Tiến sĩ'})
ON CREATE SET d1.description = 'Bằng cấp sau đại học cao nhất do Trường Đại học Sài Gòn cấp, với 05 chuyên ngành đào tạo.'
ON MATCH SET d1.description = 'Bằng cấp sau đại học cao nhất do Trường Đại học Sài Gòn cấp, với 05 chuyên ngành đào tạo.'
MERGE (u)-[:hasDegree]->(d1)
WITH u
MERGE (d2:Degree {name: 'Cao học'})
ON CREATE SET d2.description = 'Bằng cấp sau đại học do Trường Đại học Sài Gòn cấp, với 12 chuyên ngành đào tạo.'
ON MATCH SET d2.description = 'Bằng cấp sau đại học do Trường Đại học Sài Gòn cấp, với 12 chuyên ngành đào tạo.'
MERGE (u)-[:hasDegree]->(d2)
WITH u
MERGE (d3:Degree {name: 'Đại học'})
ON CREATE SET d3.description = 'Bằng cấp cử nhân do Trường Đại học Sài Gòn cấp, với 39 chương trình đào tạo.'
ON MATCH SET d3.description = 'Bằng cấp cử nhân do Trường Đại học Sài Gòn cấp, với 39 chương trình đào tạo.'
MERGE (u)-[:hasDegree]->(d3)
WITH u
MERGE (p1:Program {name: 'Chương trình đào tạo Tiến sĩ'})
ON CREATE SET p1.description = 'Chương trình đào tạo cấp bằng Tiến sĩ tại Trường Đại học Sài Gòn, bao gồm 05 chuyên ngành thuộc các lĩnh vực Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm.'
ON MATCH SET p1.description = 'Chương trình đào tạo cấp bằng Tiến sĩ tại Trường Đại học Sài Gòn, bao gồm 05 chuyên ngành thuộc các lĩnh vực Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm.'
MERGE (u)-[:offersProgram]->(p1)
WITH u
MERGE (p2:Program {name: 'Chương trình đào tạo Cao học'})
ON CREATE SET p2.description = 'Chương trình đào tạo cấp bằng Cao học tại Trường Đại học Sài Gòn, bao gồm 12 chuyên ngành thuộc các lĩnh vực Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm.'
ON MATCH SET p2.description = 'Chương trình đào tạo cấp bằng Cao học tại Trường Đại học Sài Gòn, bao gồm 12 chuyên ngành thuộc các lĩnh vực Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm.'
MERGE (u)-[:offersProgram]->(p2)
WITH u
MERGE (p3:Program {name: 'Chương trình đào tạo Đại học'})
ON CREATE SET p3.description = 'Chương trình đào tạo cấp bằng Đại học tại Trường Đại học Sài Gòn, bao gồm 39 chương trình thuộc các lĩnh vực Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm.'
ON MATCH SET p3.description = 'Chương trình đào tạo cấp bằng Đại học tại Trường Đại học Sài Gòn, bao gồm 39 chương trình thuộc các lĩnh vực Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm.'
MERGE (u)-[:offersProgram]->(p3)
WITH u
MERGE (p4:Program {name: 'Đào tạo chính quy'})
ON CREATE SET p4.description = 'Phương thức đào tạo tập trung toàn thời gian tại Trường Đại học Sài Gòn, áp dụng cho cả trình độ đại học và sau đại học.'
ON MATCH SET p4.description = 'Phương thức đào tạo tập trung toàn thời gian tại Trường Đại học Sài Gòn, áp dụng cho cả trình độ đại học và sau đại học.'
MERGE (u)-[:offersProgram]->(p4)
WITH u
MERGE (p5:Program {name: 'Giáo dục thường xuyên'})
ON CREATE SET p5.description = 'Phương thức đào tạo không tập trung tại Trường Đại học Sài Gòn, bao gồm các hình thức vừa làm vừa học, văn bằng hai, liên thông, áp dụng cho cả trình độ đại học và sau đại học.'
ON MATCH SET p5.description = 'Phương thức đào tạo không tập trung tại Trường Đại học Sài Gòn, bao gồm các hình thức vừa làm vừa học, văn bằng hai, liên thông, áp dụng cho cả trình độ đại học và sau đại học.'
MERGE (u)-[:offersProgram]->(p5)
WITH u
MERGE (p6:Program {name: 'Bồi dưỡng nghiệp vụ sư phạm'})
ON CREATE SET p6.description = 'Chương trình đào tạo cấp chứng chỉ bồi dưỡng nghiệp vụ sư phạm cho giảng viên đại học, cao đẳng và giáo viên Tiếng Anh Tiểu học tại Trường Đại học Sài Gòn, được Bộ Giáo dục và Đào tạo cho phép.'
ON MATCH SET p6.description = 'Chương trình đào tạo cấp chứng chỉ bồi dưỡng nghiệp vụ sư phạm cho giảng viên đại học, cao đẳng và giáo viên Tiếng Anh Tiểu học tại Trường Đại học Sài Gòn, được Bộ Giáo dục và Đào tạo cho phép.'
MERGE (u)-[:offersProgram]->(p6)
WITH u
MERGE (p7:Program {name: 'Chứng chỉ Công nghệ Thông tin'})
ON CREATE SET p7.description = 'Chương trình đào tạo cấp chứng chỉ Công nghệ Thông tin tại Trường Đại học Sài Gòn, được Bộ Giáo dục và Đào tạo cho phép.'
ON MATCH SET p7.description = 'Chương trình đào tạo cấp chứng chỉ Công nghệ Thông tin tại Trường Đại học Sài Gòn, được Bộ Giáo dục và Đào tạo cho phép.'
MERGE (u)-[:offersProgram]->(p7)
WITH u
MERGE (p8:Program {name: 'Chứng chỉ Tiếng Anh VSTEP'})
ON CREATE SET p8.description = 'Chương trình đào tạo cấp chứng chỉ Tiếng Anh theo khung năng lực Ngoại ngữ 6 bậc dùng cho Việt Nam (VSTEP) tại Trường Đại học Sài Gòn, được Bộ Giáo dục và Đào tạo cho phép.'
ON MATCH SET p8.description = 'Chương trình đào tạo cấp chứng chỉ Tiếng Anh theo khung năng lực Ngoại ngữ 6 bậc dùng cho Việt Nam (VSTEP) tại Trường Đại học Sài Gòn, được Bộ Giáo dục và Đào tạo cho phép.'
MERGE (u)-[:offersProgram]->(p8)