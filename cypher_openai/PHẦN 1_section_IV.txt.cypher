MERGE (university:University {name: 'Trường Đại học Sài Gòn', description: 'Trường Đại học Sài Gòn là cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo; là trường đại học đào tạo đa ngành, đa lĩnh vực. Trường Đại học Sài Gòn đào tạo từ trình độ đại học và sau đại học, theo 2 phương thức: chính quy và giáo dục thường xuyên (vừa làm vừa học, văn bằng hai, liên thông). Hiện nay, Trường đang tổ chức đào tạo 05 chuyên ngành tiến sĩ, 12 chuyên ngành cao học và 39 chương trình đào tạo trình độ đại học thuộc các lĩnh vực: Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm. Ngoài việc cấp bằng, Trường Đại học Sài Gòn được Bộ Giáo dục và Đào tạo cho phép đào tạo cấp các chứng chỉ Bồi dưỡng nghiệp vụ sư phạm cho giảng viên đại học, cao đẳng và bồi dưỡng nghiệp vụ sư phạm cho giáo viên Tiếng Anh Tiểu học, chứng chỉ Công nghệ Thông tin và chứng chỉ Tiếng Anh theo khung năng lực Ngoại ngữ 6 bậc dùng cho Việt Nam. Ngày 13/5/2017, Trường Đại học Sài Gòn được Chứng nhận kiểm định chất lượng giáo dục trường đại học. Năm 2018, Trường đón nhận Huân chương Lao động Hạng Ba do Chủ tịch nước Cộng hòa Xã hội Chủ nghĩa Việt Nam trao tặng.'})

MERGE (internationalCooperation:InternationalCooperation {name: 'Hợp tác quốc tế', description: 'Hoạt động hợp tác quốc tế tại Trường Đại học Sài Gòn bao gồm các chương trình đối ngoại và hợp tác với các trường đại học nước ngoài.'})

WITH university, internationalCooperation

MERGE (university)-[:hasInternationalCooperation]->(internationalCooperation)

MERGE (foreignRelations:InternationalCooperation {name: 'Công tác đối ngoại', description: 'Công tác đối ngoại của Trường Đại học Sài Gòn nhằm duy trì và thiết lập mối quan hệ hợp tác với các trường Đại học nước ngoài và các tổ chức quốc tế.'})
MERGE (internationalPrograms:InternationalCooperation {name: 'Các chương trình hợp tác, đào tạo quốc tế', description: 'Các chương trình hợp tác quốc tế của Trường Đại học Sài Gòn tạo điều kiện cho cán bộ, giảng viên và sinh viên học tập, nghiên cứu, trao đổi khoa học với nước ngoài.'})

WITH internationalCooperation, foreignRelations, internationalPrograms

MERGE (internationalCooperation)-[:includes]->(foreignRelations)
MERGE (internationalCooperation)-[:includes]->(internationalPrograms)

MERGE (bachelorProgram:Program {name: 'Chương trình Cử nhân Quốc tế Quản trị Kinh doanh và Quản lý Thương mại Điện tử', description: 'Chương trình liên kết đào tạo giữa trường Đại học Sài Gòn và trường Đại học Khoa học Ứng dụng IMC Krems (Cộng hòa Áo).'})
MERGE (chineseProgram:Program {name: 'Chương trình đào tạo tiếng Hoa', description: 'Chương trình liên kết với Hiệp hội Phát triển Kinh tế Văn hóa Giáo dục Đài Việt.'})
MERGE (scholarshipProgram1:Program {name: 'Học bổng toàn phần của Bộ Y tế Singapore', description: 'Học bổng toàn phần chương trình đào tạo Trợ lý bác sĩ với trị giá SGD 120,000 từ Tập đoàn Y tế Quốc gia (MOHH).'})
MERGE (scholarshipProgram2:Program {name: 'Học bổng của Bộ Giáo dục Đài Loan', description: 'Học bổng Cử nhân hệ chính quy, vừa học vừa làm đối với các Khối ngành Kinh tế, Thương mại, Thực phẩm, Dịch vụ, Công nghệ Thông tin, Kỹ thuật.'})
MERGE (trainingProgram:Program {name: 'Chương trình liên kết đào tạo khác', description: 'Ký kết hợp tác và xây dựng chương trình chuyển tiếp các ngành Công nghệ thông tin, Ngôn ngữ Anh, Sư phạm Anh, Quản trị kinh doanh, Tài chính - Ngân hàng thuộc Đại học Huddersfiled.'})

WITH internationalPrograms, bachelorProgram, chineseProgram, scholarshipProgram1, scholarshipProgram2, trainingProgram

MERGE (internationalPrograms)-[:offersProgram]->(bachelorProgram)
MERGE (internationalPrograms)-[:offersProgram]->(chineseProgram)
MERGE (internationalPrograms)-[:offersProgram]->(scholarshipProgram1)
MERGE (internationalPrograms)-[:offersProgram]->(scholarshipProgram2)
MERGE (internationalPrograms)-[:offersProgram]->(trainingProgram)