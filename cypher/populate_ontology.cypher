MERGE (university:University {name: 'Trường Đại học Sài Gòn'})
SET university.hasType = 'Cơ sở giáo dục Đại học công lập'
SET university.managedBy = 'UBND TP. Hồ Chí Minh'
SET university.offersTrainingMethod = 'Chính quy và giáo dục thường xuyên'
SET university.hasMainFields = 'Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm'
SET university.hasQualityCertification = 'Chứng nhận kiểm định chất lượng giáo dục'
SET university.hasTrainingLevels = 'Đại học, Sau đại học, Tiến sĩ'
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
MERGE (program20:TrainingProgram {name: 'Công nghệ Thông tin - Chất lượng cao'})
MERGE (postgraduateProgram1:TrainingProgram {name: 'Hóa hữu cơ - Quản trị Kinh doanh'})
MERGE (postgraduateProgram2:TrainingProgram {name: 'Hóa lý thuyết và Hóa lý - Tài chính – Ngân hàng'})
MERGE (postgraduateProgram3:TrainingProgram {name: 'Khoa học Máy tính - Toán Giải tích'})
MERGE (postgraduateProgram4:TrainingProgram {name: 'Lịch sử Việt Nam - Văn học Việt Nam'})
MERGE (postgraduateProgram5:TrainingProgram {name: 'LL & PPDH bộ môn Toán - Luật dân sự và tố tụng dân sự'})
MERGE (postgraduateProgram6:TrainingProgram {name: 'Ngôn ngữ học'})
MERGE (postgraduateProgram7:TrainingProgram {name: 'Quản lý Giáo dục'})
MERGE (doctoralProgram1:TrainingProgram {name: 'Hóa hữu cơ'})
MERGE (doctoralProgram2:TrainingProgram {name: 'Lịch sử Việt Nam'})
MERGE (doctoralProgram3:TrainingProgram {name: 'Quản lý Giáo dục'})
MERGE (doctoralProgram4:TrainingProgram {name: 'Toán Giải tích'})
MERGE (doctoralProgram5:TrainingProgram {name: 'Quản trị Kinh doanh'})
MERGE (university)-[:hasPrograms]->(program1)
MERGE (university)-[:hasPrograms]->(program2)
MERGE (university)-[:hasPrograms]->(program3)
MERGE (university)-[:hasPrograms]->(program4)
MERGE (university)-[:hasPrograms]->(program5)
MERGE (university)-[:hasPrograms]->(program6)
MERGE (university)-[:hasPrograms]->(program7)
MERGE (university)-[:hasPrograms]->(program8)
MERGE (university)-[:hasPrograms]->(program9)
MERGE (university)-[:hasPrograms]->(program10)
MERGE (university)-[:hasPrograms]->(program11)
MERGE (university)-[:hasPrograms]->(program12)
MERGE (university)-[:hasPrograms]->(program13)
MERGE (university)-[:hasPrograms]->(program14)
MERGE (university)-[:hasPrograms]->(program15)
MERGE (university)-[:hasPrograms]->(program16)
MERGE (university)-[:hasPrograms]->(program17)
MERGE (university)-[:hasPrograms]->(program18)
MERGE (university)-[:hasPrograms]->(program19)
MERGE (university)-[:hasPrograms]->(program20)
MERGE (university)-[:hasPrograms]->(postgraduateProgram1)
MERGE (university)-[:hasPrograms]->(postgraduateProgram2)
MERGE (university)-[:hasPrograms]->(postgraduateProgram3)
MERGE (university)-[:hasPrograms]->(postgraduateProgram4)
MERGE (university)-[:hasPrograms]->(postgraduateProgram5)
MERGE (university)-[:hasPrograms]->(postgraduateProgram6)
MERGE (university)-[:hasPrograms]->(postgraduateProgram7)
MERGE (university)-[:hasPrograms]->(doctoralProgram1)
MERGE (university)-[:hasPrograms]->(doctoralProgram2)
MERGE (university)-[:hasPrograms]->(doctoralProgram3)
MERGE (university)-[:hasPrograms]->(doctoralProgram4)
MERGE (university)-[:hasPrograms]->(doctoralProgram5)
SET university.offersTrainingMethod = 'Giáo dục thường xuyên (vừa làm vừa học, Liên kết đào tạo, Liên thông, Bằng hai)'
MERGE (program21:TrainingProgram {name: 'Đào tạo Đại học liên thông Công nghệ Thông tin'})
MERGE (program22:TrainingProgram {name: 'Đào tạo Đại học liên thông Kế toán'})
MERGE (program23:TrainingProgram {name: 'Đào tạo Đại học liên thông Quản trị Kinh doanh'})
MERGE (program24:TrainingProgram {name: 'Đào tạo Đại học liên thông Giáo dục Mầm non'})
MERGE (program25:TrainingProgram {name: 'Đào tạo Đại học liên thông Giáo dục Tiểu học'})
MERGE (program26:TrainingProgram {name: 'Đào tạo văn bằng thứ hai Ngôn ngữ Anh'})
MERGE (program27:TrainingProgram {name: 'Đào tạo văn bằng thứ hai Kế toán'})
MERGE (program28:TrainingProgram {name: 'Đào tạo văn bằng thứ hai Luật'})
MERGE (program29:TrainingProgram {name: 'Đào tạo văn bằng thứ hai Quản trị Kinh doanh'})
MERGE (program30:TrainingProgram {name: 'Đào tạo văn bằng thứ hai Giáo dục Tiểu học'})
MERGE (program31:TrainingProgram {name: 'Đào tạo văn bằng thứ hai Quản lý Giáo dục'})
MERGE (program32:TrainingProgram {name: 'Đào tạo hệ đại học vừa làm vừa học Quản trị Kinh doanh'})
MERGE (program33:TrainingProgram {name: 'Đào tạo hệ đại học vừa làm vừa học Tài chính - Ngân hàng'})
MERGE (program34:TrainingProgram {name: 'Đào tạo hệ đại học vừa làm vừa học Tài chính - Kế toán'})
MERGE (program35:TrainingProgram {name: 'Đào tạo hệ đại học vừa làm vừa học Luật'})
MERGE (program36:TrainingProgram {name: 'Đào tạo hệ đại học vừa làm vừa học Giáo dục Tiểu học'})
MERGE (program37:TrainingProgram {name: 'Đào tạo hệ đại học vừa làm vừa học Giáo dục Mầm non'})
MERGE (university)-[:hasPrograms]->(program21)
MERGE (university)-[:hasPrograms]->(program22)
MERGE (university)-[:hasPrograms]->(program23)
MERGE (university)-[:hasPrograms]->(program24)
MERGE (university)-[:hasPrograms]->(program25)
MERGE (university)-[:hasPrograms]->(program26)
MERGE (university)-[:hasPrograms]->(program27)
MERGE (university)-[:hasPrograms]->(program28)
MERGE (university)-[:hasPrograms]->(program29)
MERGE (university)-[:hasPrograms]->(program30)
MERGE (university)-[:hasPrograms]->(program31)
MERGE (university)-[:hasPrograms]->(program32)
MERGE (university)-[:hasPrograms]->(program33)
MERGE (university)-[:hasPrograms]->(program34)
MERGE (university)-[:hasPrograms]->(program35)
MERGE (university)-[:hasPrograms]->(program36)
MERGE (university)-[:hasPrograms]->(program37)
MERGE (campus1:Campus {name: 'Cơ sở 273 An Dương Vương, Q.5'})
SET campus1.area = '42.743 m2'
MERGE (campus2:Campus {name: 'Cơ sở 105 Bà Huyện Thanh Quan, Q.3'})
SET campus2.area = '4.823 m2'
MERGE (campus3:Campus {name: 'Cơ sở 04 Tôn Đức Thắng, Q.1'})
SET campus3.area = '19.655 m2'
MERGE (dormitory:Campus {name: 'Ký túc xá 99 An Dương Vương, Q.8'})
SET dormitory.area = '4.800 m2'
MERGE (university)-[:hasCampus]->(campus1)
MERGE (university)-[:hasCampus]->(campus2)
MERGE (university)-[:hasCampus]->(campus3)
MERGE (university)-[:hasCampus]->(dormitory)
SET university.hasInternationalCooperation = 'Hợp tác với các trường Đại học nước ngoài và các tổ chức quốc tế'
SET university.hasInternationalBachelorProgram = 'Chương trình Cử nhân Quốc tế Quản trị Kinh doanh và Quản lý Thương mại Điện tử'
MERGE (program38:TrainingProgram {name: 'Chương trình liên kết đào tạo Cử nhân Quản trị Kinh doanh và Quản lý Thương mại Điện tử'})
SET program38.implementedBy = 'Trường Đại học Sài Gòn và trường Đại học Khoa học Ứng dụng IMC Krems'
SET program38.decisionNumber = '1498/QĐ-BGDĐT'
SET program38.decisionDate = '28/4/2014'
MERGE (program39:TrainingProgram {name: 'Chương trình đào tạo tiếng Hoa'})
SET program39.linkedWith = 'Hiệp hội Phát triển Kinh tế Văn hóa Giáo dục Đài Việt'
SET program39.contents = 'Hoa ngữ giao tiếp, Luyện thi TOCFL, Hoa ngữ lớp Online'
SET program39.certificationBy = 'Trung tâm Hoa Ngữ Sư Phạm Đài Loan'
MERGE (scholarship1:Scholarship {name: 'Học bổng toàn phần của Bộ Y tế Singapore - Asian Nursing Scholarship'})
SET scholarship1.details = 'Học bổng toàn phần chương trình đào tạo Trợ lý bác sĩ trong thời gian 3 năm với trị giá SGD 120,000'
SET scholarship1.benefits = 'Trợ cấp sinh hoạt phí từ SGD 720/tháng, hỗ trợ ký túc xá, chi phí đi lại, dịch vụ y tế'
MERGE (scholarship2:Scholarship {name: 'Học bổng của Bộ Giáo dục Đài Loan'})
SET scholarship2.details = 'Học bổng Cử nhân hệ chính quy, vừa học vừa làm đối với các Khối ngành Kinh tế, Thương mại, Thực phẩm, Dịch vụ, Công nghệ Thông tin, Kỹ thuật'
SET scholarship2.benefits = 'Miễn giảm học phí, phí ký túc xá, thực tập có lương'
MERGE (trainingLink1:TrainingProgram {name: 'Chương trình chuyển tiếp Công nghệ thông tin'})
MERGE (trainingLink2:TrainingProgram {name: 'Chương trình chuyển tiếp Ngôn ngữ Anh'})
MERGE (trainingLink3:TrainingProgram {name: 'Chương trình chuyển tiếp Sư phạm Anh'})
MERGE (trainingLink4:TrainingProgram {name: 'Chương trình chuyển tiếp Quản trị kinh doanh'})
MERGE (trainingLink5:TrainingProgram {name: 'Chương trình chuyển tiếp Tài chính - Ngân hàng'})
MERGE (university)-[:hasPrograms]->(program38)
MERGE (university)-[:hasPrograms]->(program39)
MERGE (university)-[:hasScholarshipPrograms]->(scholarship1)
MERGE (university)-[:hasScholarshipPrograms]->(scholarship2)
MERGE (university)-[:hasTrainingLinks]->(trainingLink1)
MERGE (university)-[:hasTrainingLinks]->(trainingLink2)
MERGE (university)-[:hasTrainingLinks]->(trainingLink3)
MERGE (university)-[:hasTrainingLinks]->(trainingLink4)
MERGE (university)-[:hasTrainingLinks]->(trainingLink5)
MERGE (researchTopic:ResearchTopic {name: 'Nghiên cứu khoa học cấp cơ sở'})
SET researchTopic.conditions = 'Có kết quả học tập trung bình trở lên, không bị kỷ luật, không có đề tài bị hủy hoặc nghiệm thu không đạt'
SET researchTopic.benefits = 'Hỗ trợ kinh phí, cộng điểm rèn luyện, cấp giấy chứng nhận NCKH, thưởng kinh phí cho đề tài tốt và xuất sắc'
MERGE (journal:Journal {name: 'Tạp chí Khoa học Đại học Sài Gòn'})
SET journal.managedBy = 'Trường Đại học Sài Gòn'
SET journal.servesAudience = 'Cán bộ giảng dạy, nghiên cứu, quản lý, sinh viên các trường đại học, cao đẳng, các viện, học viện, các trung tâm nghiên cứu'
SET journal.purpose = 'Diễn đàn khoa học công bố kết quả nghiên cứu và hoạt động khoa học của cán bộ, giảng viên'
MERGE (university)-[:hasResearchConditions]->(researchTopic)
MERGE (university)-[:hasQualityCertification]->(journal)
SET journal.issn = '1859-3208'
SET journal.license = 'Số 22/GP-BTTTT do Bộ Thông tin và Truyền thông cấp ngày 23/01/2015'
SET journal.contactInfo = 'Điện thoại: (028) 38 321 360, Email: tcdhsg@sgu.edu.vn, Website: http://sj.sgu.edu.vn/'
SET journal.hasArticleRegulations = 'Phải nêu rõ mục tiêu nghiên cứu, có kết quả mới, được phản biện, có danh mục chú thích và tài liệu tham khảo'
SET journal.technicalRequirements = 'Bài viết không quá 12 trang A4, soạn thảo trên Word, bảng mã Unicode, Font Times New Roman, cỡ chữ 13'
SET journal.hasCitationGuidelines = 'Trích dẫn và danh mục Tài liệu tham khảo theo tiêu chuẩn IEEE hoặc APA'
SET journal.imageRequirements = 'Hình minh họa cần rõ ràng, 300 dpi hoặc cao hơn, định dạng EPS, PDF, AI, PNG, JPG, BMP'
SET journal.submissionEmail = 'tcdhsg@sgu.edu.vn'
SET journal.contactPhone = '028.38 321 360'
SET journal.editingOfficeAddress = 'Ban Biên tập Tạp chí Khoa học Đại học Sài Gòn, phòng C010 – Trường Đại học Sài Gòn, số 273 An Dương Vương, phường 3, quận 5, Thành phố Hồ Chí Minh'
MERGE (trainingInfo:TrainingProgram {name: 'Thông tin đào tạo'})
SET trainingInfo.classSchedule = 'Ca 1: 07g00 đến 07g50, Ca 2: 07g50 đến 08g40, Ca 3: 09g00 đến 09g50, Nghỉ 20 phút giữa các ca'
SET trainingInfo.classroomCodes = 'C: cơ sở chính, 1: cơ sở 1, 2: cơ sở 2'
SET trainingInfo.registrationSystem = 'daotao.sgu.edu.vn'
SET trainingInfo.trainingInfoPage = 'thongtindaotao.sgu.edu.vn'
MERGE (university)-[:hasTrainingLinks]->(trainingInfo)