MERGE (university:University {name: 'Trường Đại học Sài Gòn'})
SET university.hasType = 'Công lập',
university.managedBy = 'UBND TP. Hồ Chí Minh',
university.offersTrainingMethod = 'Chính quy, Giáo dục thường xuyên',
university.hasMainFields = 'Kinh tế, Kỹ thuật, Công nghệ, Văn hóa xã hội, Chính trị, Nghệ thuật, Sư phạm',
university.hasQualityCertification = 'Chứng nhận kiểm định chất lượng giáo dục',
university.hasTrainingLevels = 'Đại học, Sau đại học, Tiến sĩ'
WITH university
MERGE (program1:TrainingProgram {name: 'Giáo dục Chính trị - Du lịch'})
MERGE (program2:TrainingProgram {name: 'Giáo dục Mầm non - Kế toán'})
MERGE (program3:TrainingProgram {name: 'Giáo dục Tiểu học - Khoa học Môi trường'})
MERGE (program4:TrainingProgram {name: 'Sư phạm Âm nhạc - Kinh doanh Quốc tế'})
MERGE (program5:TrainingProgram {name: 'Sư phạm Địa lý - Kỹ thuật Điện'})
MERGE (program6:TrainingProgram {name: 'Sư phạm Hóa học - Kỹ thuật Điện tử - Viễn thông'})
MERGE (program7:TrainingProgram {name: 'Sư phạm Khoa học Tự nhiên - Kỹ thuật Phần mềm'})
MERGE (program8:TrainingProgram {name: 'Sư phạm Lịch sử - Luật'})
MERGE (program9:TrainingProgram {name: 'Sư phạm Lịch sử - Địa lý - Ngôn ngữ Anh'})
MERGE (program10:TrainingProgram {name: 'Sư phạm Mỹ thuật - Quản lý Giáo dục'})
MERGE (program11:TrainingProgram {name: 'Sư phạm Ngữ Văn - Quản trị Kinh doanh'})
MERGE (program12:TrainingProgram {name: 'Sư phạm Sinh học - Quản trị Văn phòng'})
MERGE (program13:TrainingProgram {name: 'Sư phạm Tiếng Anh - Quốc tế học'})
MERGE (program14:TrainingProgram {name: 'Sư phạm Toán học - Tài chính - Ngân hàng'})
MERGE (program15:TrainingProgram {name: 'Sư phạm Vật lý - Tâm lý học'})
MERGE (program16:TrainingProgram {name: 'CNKT Điện tử - Viễn thông - Thanh nhạc'})
MERGE (program17:TrainingProgram {name: 'CNKT Điện, Điện tử - Thông tin - Thư viện'})
MERGE (program18:TrainingProgram {name: 'Công nghệ Kỹ thuật Môi trường - Toán Ứng dụng'})
MERGE (program19:TrainingProgram {name: 'Công nghệ Thông tin - Việt Nam học'})
MERGE (program20:TrainingProgram {name: 'Chương trình chất lượng cao: Công nghệ Thông tin'})
WITH university,
[program1, program2, program3, program4, program5, program6, program7, program8, program9, program10, program11, program12, program13, program14, program15, program16, program17, program18, program19, program20] AS programs
FOREACH (program IN programs |
MERGE (university)-[:hasPrograms]->(program)
)
WITH 'Trường Đại học Sài Gòn' AS universityName
MERGE (university:University {name: universityName})
WITH university
MERGE (program21:TrainingProgram {name: 'Giáo dục thường xuyên'})
MERGE (program22:TrainingProgram {name: 'Đào tạo Đại học liên thông'})
MERGE (program23:TrainingProgram {name: 'Đào tạo văn bằng thứ hai'})
MERGE (program24:TrainingProgram {name: 'Đào tạo hệ đại học vừa làm vừa học'})
WITH university, [program21, program22, program23, program24] AS programs
FOREACH (program IN programs |
MERGE (university)-[:hasPrograms]->(program)
)
MERGE (campus1:Campus {name: 'Cơ sở 273 An Dương Vương, Q.5', area: '42.743 m2'})
MERGE (campus2:Campus {name: 'Cơ sở 105 Bà Huyện Thanh Quan, Q.3', area: '4.823 m2'})
MERGE (campus3:Campus {name: 'Cơ sở 04 Tôn Đức Thắng, Q.1', area: '19.655 m2'})
MERGE (dormitory:Campus {name: 'Ký túc xá 99 An Dương Vương, Q.8', area: '4.800 m2'})
WITH university, [campus1, campus2, campus3, dormitory] AS campuses
FOREACH (campus IN campuses |
MERGE (university)-[:hasCampus]->(campus)
)
MERGE (internationalCoop:InternationalCooperation {name: 'Hợp tác quốc tế'})
SET internationalCoop.description = 'Hợp tác với các trường Đại học nước ngoài và các tổ chức quốc tế'
MERGE (university)-[:hasInternationalCooperation]->(internationalCoop)
MERGE (program25:TrainingProgram {name: 'Cử nhân Quốc tế Quản trị Kinh doanh và Quản lý Thương mại Điện tử'})
SET program25.description = 'Liên kết đào tạo giữa trường Đại học Sài Gòn và trường Đại học Khoa học Ứng dụng IMC Krems (Cộng hòa Áo)'
MERGE (university)-[:hasPrograms]->(program25)
WITH 'Trường Đại học Sài Gòn' AS universityName
MERGE (university:University {name: universityName})
WITH university
MERGE (program26:TrainingProgram {name: 'Chương trình liên kết đào tạo Cử nhân Quản trị Kinh doanh và Quản lý Thương mại Điện tử'})
SET program26.description = 'Triển khai theo Quyết định số 1498/QĐ-BGDĐT ngày 28/4/2014 của Bộ trưởng Bộ Giáo dục và Đào tạo'
MERGE (university)-[:hasPrograms]->(program26)
MERGE (program27:TrainingProgram {name: 'Chương trình đào tạo tiếng Hoa'})
SET program27.description = 'Liên kết với Hiệp hội Phát triển Kinh tế Văn hóa Giáo dục Đài Việt'
MERGE (university)-[:hasPrograms]->(program27)
MERGE (scholarship1:Scholarship {name: 'Học bổng toàn phần của Bộ Y tế Singapore - Asian Nursing Scholarship'})
SET scholarship1.details = 'Học bổng toàn phần chương trình đào tạo Trợ lý bác sĩ trong thời gian 3 năm với trị giá SGD 120,000'
MERGE (university)-[:hasScholarshipPrograms]->(scholarship1)
MERGE (scholarship2:Scholarship {name: 'Học bổng của Bộ Giáo dục Đài Loan'})
SET scholarship2.details = 'Học bổng Cử nhân hệ chính quy, vừa học vừa làm đối với các Khối ngành Kinh tế, Thương mại, Thực phẩm, Dịch vụ, Công nghệ Thông tin, Kỹ thuật'
MERGE (university)-[:hasScholarshipPrograms]->(scholarship2)
MERGE (program28:TrainingProgram {name: 'Chương trình liên kết đào tạo các ngành Công nghệ thông tin, Ngôn ngữ Anh, Sư phạm Anh, Quản trị kinh doanh, Tài chính - Ngân hàng'})
SET program28.details = 'Ký kết hợp tác và xây dựng chương trình chuyển tiếp'
MERGE (university)-[:hasPrograms]->(program28)
MERGE (program29:TrainingProgram {name: 'Thạc sĩ Giảng dạy tiếng Anh (Master of TESOL)'})
SET program29.details = 'Trao đổi thông tin, lên kế hoạch liên kết chương trình với Đại học Huddersfiled (Vương quốc Anh)'
MERGE (university)-[:hasPrograms]->(program29)
WITH 'Trường Đại học Sài Gòn' AS universityName
MERGE (university:University {name: universityName})
WITH university
MERGE (researchTopic:ResearchTopic {name: 'Nghiên cứu khoa học cấp cơ sở'})
SET researchTopic.details = 'Sinh viên tham gia thực hiện đề tài trong thời gian từ 06 – 09 tháng dưới sự hướng dẫn của Giảng viên'
MERGE (university)-[:hasPrograms]->(researchTopic)
MERGE (benefit1:ResearchTopic {name: 'Quyền lợi NCKH'})
SET benefit1.details = 'Đối với các đề tài có kết quả nghiệm thu đạt trở lên sẽ được hỗ trợ kinh phí, cộng điểm rèn luyện năm học và cấp giấy chứng nhận NCKH'
MERGE (university)-[:hasPrograms]->(benefit1)
MERGE (benefit2:ResearchTopic {name: 'Bài báo Khoa học và báo cáo tham luận Hội thảo'})
SET benefit2.details = 'Sinh viên có bài báo đăng trên các Tạp chí chuyên ngành trong nước, quốc tế hoặc báo cáo khoa học đăng trên kỷ yếu các Hội thảo'
MERGE (university)-[:hasPrograms]->(benefit2)
MERGE (journal:Journal {name: 'Tạp chí Khoa học Đại học Sài Gòn'})
SET journal.managedBy = 'Trường Đại học Sài Gòn',
journal.servesAudience = 'Cán bộ giảng dạy, nghiên cứu, quản lý, sinh viên các trường đại học, cao đẳng, các viện, học viện, các trung tâm nghiên cứu'
MERGE (university)-[:hasPrograms]->(journal)
WITH 'Trường Đại học Sài Gòn' AS universityName
MERGE (university:University {name: universityName})
WITH university
MERGE (journal:Journal {name: 'Tạp chí Khoa học Đại học Sài Gòn'})
SET journal.managedBy = 'Trường Đại học Sài Gòn',
journal.ISSN = '1859-3208',
journal.hasArticleRegulations = 'Phải nêu rõ mục tiêu nghiên cứu; cần có các kết quả mới, có giá trị khoa học và thực tiễn',
journal.usesCitationStandard = 'IEEE, APA',
journal.servesAudience = 'Cán bộ giảng dạy, nghiên cứu, quản lý, sinh viên các trường đại học, cao đẳng, các viện, học viện, các trung tâm nghiên cứu'
MERGE (university)-[:hasPrograms]->(journal)
SET journal.contactInfo = 'Điện thoại: (028) 38 321 360, Email: tcdhsg@sgu.edu.vn, Website: http://sj.sgu.edu.vn/'
MERGE (regulation:ResearchTopic {name: 'Quy định chung về bài báo khoa học'})
SET regulation.details = 'Phải nêu rõ mục tiêu nghiên cứu; cần có các kết quả mới, có giá trị khoa học và thực tiễn trong lĩnh vực nghiên cứu'
MERGE (university)-[:hasPrograms]->(regulation)
MERGE (submissionGuideline:ResearchTopic {name: 'Thể lệ gửi bài đăng tạp chí Khoa học Đại Học Sài Gòn'})
SET submissionGuideline.details = 'Bài gửi đăng trên Tạp chí phải là công trình khoa học, các báo cáo học thuật hoặc kết quả thực hiện đề tài khoa học mới'
MERGE (university)-[:hasPrograms]->(submissionGuideline)
WITH 'Trường Đại học Sài Gòn' AS universityName
MERGE (university:University {name: universityName})
WITH university
MERGE (submissionGuideline:ResearchTopic {name: 'Hướng dẫn gửi bài'})
SET submissionGuideline.details = 'Hình minh họa cần rõ ràng, gửi kèm file ảnh, hình cùng với toàn văn bài viết'
MERGE (university)-[:hasPrograms]->(submissionGuideline)
MERGE (trainingInfo:ResearchTopic {name: 'Thông tin đào tạo'})
SET trainingInfo.details = 'Quy định về số tiết và thời gian của các tiết học trong ngày, thông tin về mã phòng học'
MERGE (university)-[:hasPrograms]->(trainingInfo)
MERGE (trainingPage:ResearchTopic {name: 'Trang Phòng Đào tạo'})
SET trainingPage.details = 'Cổng thông tin giữa Nhà trường và sinh viên, phụ huynh về các hoạt động đào tạo'
MERGE (university)-[:hasPrograms]->(trainingPage)
MERGE (infoPage:ResearchTopic {name: 'Trang Thông tin Đào tạo'})
SET infoPage.details = 'Đăng kí môn học, cung cấp thông tin liên quan đến công tác đào tạo đến sinh viên'
MERGE (university)-[:hasPrograms]->(infoPage)