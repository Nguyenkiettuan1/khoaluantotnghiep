MERGE (university:University {name: 'Trường Đại học Sài Gòn', description: 'Trường Đại học Sài Gòn là cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo; là trường đại học đào tạo đa ngành, đa lĩnh vực. Trường Đại học Sài Gòn đào tạo từ trình độ đại học và sau đại học, theo 2 phương thức: chính quy và giáo dục thường xuyên (vừa làm vừa học, văn bằng hai, liên thông). Hiện nay, Trường đang tổ chức đào tạo 05 chuyên ngành tiến sĩ, 12 chuyên ngành cao học và 39 chương trình đào tạo trình độ đại học thuộc các lĩnh vực: Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm. Ngoài việc cấp bằng, Trường Đại học Sài Gòn được Bộ Giáo dục và Đào tạo cho phép đào tạo cấp các chứng chỉ Bồi dưỡng nghiệp vụ sư phạm cho giảng viên đại học, cao đẳng và bồi dưỡng nghiệp vụ sư phạm cho giáo viên Tiếng Anh Tiểu học, chứng chỉ Công nghệ Thông tin và chứng chỉ Tiếng Anh theo khung năng lực Ngoại ngữ 6 bậc dùng cho Việt Nam. Ngày 13/5/2017, Trường Đại học Sài Gòn được Chứng nhận kiểm định chất lượng giáo dục trường đại học. Năm 2018, Trường đón nhận Huân chương Lao động Hạng Ba do Chủ tịch nước Cộng hòa Xã hội Chủ nghĩa Việt Nam trao tặng.'})

MERGE (organization:Organization {name: 'Tổ chức quản lý', description: 'Tổ chức quản lý giáo dục của Trường Đại học Sài Gòn.'})
MERGE (university)-[:hasManagement]->(organization)

MERGE (program1:Program {name: 'Chương trình đào tạo 1', description: 'Chương trình đào tạo trình độ đại học thuộc lĩnh vực Kinh tế - Kỹ thuật - Công nghệ.'})
MERGE (program2:Program {name: 'Chương trình đào tạo 2', description: 'Chương trình đào tạo trình độ đại học thuộc lĩnh vực Văn hóa xã hội.'})
MERGE (university)-[:offersPrograms]->(program1)
MERGE (university)-[:offersPrograms]->(program2)

MERGE (department1:Department {name: 'Khoa Kinh tế', description: 'Khoa Kinh tế của Trường Đại học Sài Gòn chuyên đào tạo các chuyên ngành liên quan đến kinh tế.'})
MERGE (department2:Department {name: 'Khoa Kỹ thuật', description: 'Khoa Kỹ thuật của Trường Đại học Sài Gòn chuyên đào tạo các chuyên ngành liên quan đến kỹ thuật.'})
MERGE (university)-[:hasDepartments]->(department1)
MERGE (university)-[:hasDepartments]->(department2)

MERGE (scholarship:Scholarship {name: 'Chứng chỉ Bồi dưỡng nghiệp vụ sư phạm', description: 'Chứng chỉ Bồi dưỡng nghiệp vụ sư phạm cho giảng viên đại học, cao đẳng.'})
MERGE (university)-[:awardedScholarships]->(scholarship)

MERGE (award:Award {name: 'Huân chương Lao động Hạng Ba', description: 'Huân chương Lao động Hạng Ba do Chủ tịch nước Cộng hòa Xã hội Chủ nghĩa Việt Nam trao tặng cho Trường Đại học Sài Gòn.'})
MERGE (university)-[:hasAwards]->(award)

MERGE (research:Research {name: 'Dự án nghiên cứu 1', description: 'Dự án nghiên cứu tại Trường Đại học Sài Gòn.'})
MERGE (university)-[:hasResearchProjects]->(research)

MERGE (internationalCooperation:InternationalCooperation {name: 'Hợp tác quốc tế', description: 'Hợp tác quốc tế của Trường Đại học Sài Gòn với các tổ chức giáo dục khác.'})
MERGE (university)-[:hasInternationalCooperations]->(internationalCooperation)