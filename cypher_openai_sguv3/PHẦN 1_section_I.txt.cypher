MERGE (university:University {name: 'Trường Đại học Sài Gòn', description: 'Trường Đại học Sài Gòn là cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo; là trường đại học đào tạo đa ngành, đa lĩnh vực. Trường Đại học Sài Gòn đào tạo từ trình độ đại học và sau đại học, theo 2 phương thức: chính quy và giáo dục thường xuyên (vừa làm vừa học, văn bằng hai, liên thông). Hiện nay, Trường đang tổ chức đào tạo 05 chuyên ngành tiến sĩ, 12 chuyên ngành cao học và 39 chương trình đào tạo trình độ đại học thuộc các lĩnh vực: Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm. Ngoài việc cấp bằng, Trường Đại học Sài Gòn được Bộ Giáo dục và Đào tạo cho phép đào tạo cấp các chứng chỉ Bồi dưỡng nghiệp vụ sư phạm cho giảng viên đại học, cao đẳng và bồi dưỡng nghiệp vụ sư phạm cho giáo viên Tiếng Anh Tiểu học, chứng chỉ Công nghệ Thông tin và chứng chỉ Tiếng Anh theo khung năng lực Ngoại ngữ 6 bậc dùng cho Việt Nam. Ngày 13/5/2017, Trường Đại học Sài Gòn được Chứng nhận kiểm định chất lượng giáo dục trường đại học. Năm 2018, Trường đón nhận Huân chương Lao động Hạng Ba do Chủ tịch nước Cộng hòa Xã hội Chủ nghĩa Việt Nam trao tặng.'})

MERGE (bachelorDegree:Degree {name: 'Cử nhân', description: 'Bằng cử nhân là bằng cấp được cấp cho sinh viên hoàn thành chương trình đào tạo đại học.'})
MERGE (masterDegree:Degree {name: 'Thạc sĩ', description: 'Bằng thạc sĩ là bằng cấp được cấp cho sinh viên hoàn thành chương trình đào tạo sau đại học.'})
MERGE (doctoralDegree:Degree {name: 'Tiến sĩ', description: 'Bằng tiến sĩ là bằng cấp cao nhất trong hệ thống giáo dục đại học.'})

MERGE (regularProgram:Program {name: 'Chương trình chính quy', description: 'Chương trình đào tạo chính quy dành cho sinh viên học tập toàn thời gian.'})
MERGE (continuingEducationProgram:Program {name: 'Chương trình giáo dục thường xuyên', description: 'Chương trình đào tạo dành cho người học vừa làm vừa học.'})
MERGE (highQualityProgram:Program {name: 'Chương trình chất lượng cao', description: 'Chương trình đào tạo chất lượng cao với tiêu chuẩn quốc tế.'})

MERGE (department1:Department {name: 'Khoa Kinh tế', description: 'Khoa Kinh tế đào tạo các chuyên ngành liên quan đến kinh tế và quản trị.'})
MERGE (department2:Department {name: 'Khoa Kỹ thuật', description: 'Khoa Kỹ thuật đào tạo các chuyên ngành kỹ thuật và công nghệ.'})
MERGE (department3:Department {name: 'Khoa Nghệ thuật', description: 'Khoa Nghệ thuật đào tạo các chuyên ngành nghệ thuật và thiết kế.'})

MERGE (researchProject1:Research {name: 'Dự án nghiên cứu 1', description: 'Dự án nghiên cứu về phát triển bền vững.'})
MERGE (researchProject2:Research {name: 'Dự án nghiên cứu 2', description: 'Dự án nghiên cứu về công nghệ thông tin.'})

MERGE (cooperation1:InternationalCooperation {name: 'Hợp tác quốc tế 1', description: 'Hợp tác với các trường đại học quốc tế trong lĩnh vực giáo dục.'})
MERGE (cooperation2:InternationalCooperation {name: 'Hợp tác quốc tế 2', description: 'Hợp tác nghiên cứu với các tổ chức quốc tế.'})

MERGE (journal1:Journal {name: 'Tạp chí Khoa học', description: 'Tạp chí khoa học công bố các nghiên cứu và bài viết trong lĩnh vực giáo dục và nghiên cứu.'})

MERGE (student1:Student {name: 'Sinh viên 1', description: 'Sinh viên đang theo học tại Trường Đại học Sài Gòn.'})
MERGE (student2:Student {name: 'Sinh viên 2', description: 'Sinh viên đang theo học tại Trường Đại học Sài Gòn.'})

MERGE (faculty1:Faculty {name: 'Giảng viên 1', description: 'Giảng viên có nhiều năm kinh nghiệm trong lĩnh vực giảng dạy.'})
MERGE (faculty2:Faculty {name: 'Giảng viên 2', description: 'Giảng viên chuyên ngành Kỹ thuật với nhiều nghiên cứu nổi bật.'})

WITH university, bachelorDegree, masterDegree, doctoralDegree, regularProgram, continuingEducationProgram, highQualityProgram, department1, department2, department3, researchProject1, researchProject2, cooperation1, cooperation2, journal1, student1, student2, faculty1, faculty2

MERGE (university)-[:hasDegree]->(bachelorDegree)
MERGE (university)-[:hasDegree]->(masterDegree)
MERGE (university)-[:hasDegree]->(doctoralDegree)

MERGE (university)-[:offersProgram]->(regularProgram)
MERGE (university)-[:offersProgram]->(continuingEducationProgram)
MERGE (university)-[:offersProgram]->(highQualityProgram)

MERGE (university)-[:hasDepartment]->(department1)
MERGE (university)-[:hasDepartment]->(department2)
MERGE (university)-[:hasDepartment]->(department3)

MERGE (university)-[:conductsResearch]->(researchProject1)
MERGE (university)-[:conductsResearch]->(researchProject2)

MERGE (university)-[:hasInternationalCooperation]->(cooperation1)
MERGE (university)-[:hasInternationalCooperation]->(cooperation2)

MERGE (university)-[:publishesIn]->(journal1)

MERGE (university)-[:hasStudent]->(student1)
MERGE (university)-[:hasStudent]->(student2)

MERGE (university)-[:hasFaculty]->(faculty1)
MERGE (university)-[:hasFaculty]->(faculty2)