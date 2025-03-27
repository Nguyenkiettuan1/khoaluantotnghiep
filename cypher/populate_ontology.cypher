MERGE (university:University {name: 'Trường Đại học Sài Gòn', description: 'Cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo; là trường đại học đào tạo đa ngành, đa lĩnh vực. Trường Đại học Sài Gòn đào tạo từ trình độ đại học và sau đại học, theo 2 phương thức: chính quy và giáo dục thường xuyên (vừa làm vừa học, văn bằng hai, liên thông). Hiện nay, Trường đang tổ chức đào tạo 05 chuyên ngành tiến sĩ, 12 chuyên ngành cao học và 39 chương trình đào tạo trình độ đại học thuộc các lĩnh vực: Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm. Ngoài việc cấp bằng, Trường Đại học Sài Gòn được Bộ Giáo dục và Đào tạo cho phép đào tạo cấp các chứng chỉ Bồi dưỡng nghiệp vụ sư phạm cho giảng viên đại học, cao đẳng và bồi dưỡng nghiệp vụ sư phạm cho giáo viên Tiếng Anh Tiểu học, chứng chỉ Công nghệ Thông tin và chứng chỉ Tiếng Anh theo khung năng lực Ngoại ngữ 6 bậc dùng cho Việt Nam. Ngày 13/5/2017, Trường Đại học Sài Gòn được Chứng nhận kiểm định chất lượng giáo dục trường đại học. Năm 2018, Trường đón nhận Huân chương Lao động Hạng Ba do Chủ tịch nước Cộng hòa Xã hội Chủ nghĩa Việt Nam trao tặng.'})

MERGE (qualityCertification:QualityAssurance {name: 'Chứng nhận kiểm định chất lượng giáo dục', description: 'Chứng nhận kiểm định chất lượng giáo dục trường đại học được cấp cho Trường Đại học Sài Gòn vào ngày 13/5/2017.'})
MERGE (university)-[:hasQualityAssurance]->(qualityCertification)

MERGE (campus1:Campus {name: 'Campus 1', description: 'Khuôn viên chính của Trường Đại học Sài Gòn, nơi diễn ra nhiều hoạt động học tập và nghiên cứu.'})
MERGE (campus2:Campus {name: 'Campus 2', description: 'Khuôn viên phụ của Trường Đại học Sài Gòn, phục vụ cho các chương trình đào tạo khác nhau.'})
MERGE (university)-[:hasCampus]->(campus1)
MERGE (university)-[:hasCampus]->(campus2)

MERGE (student1:Student {name: 'Sinh viên 1', description: 'Sinh viên đang theo học tại Trường Đại học Sài Gòn.'})
MERGE (student2:Student {name: 'Sinh viên 2', description: 'Sinh viên đang theo học tại Trường Đại học Sài Gòn.'})
MERGE (university)-[:hasStudent]->(student1)
MERGE (university)-[:hasStudent]->(student2)

MERGE (scholarship1:Scholarship {name: 'Học bổng 1', description: 'Học bổng dành cho sinh viên xuất sắc tại Trường Đại học Sài Gòn.'})
MERGE (scholarship2:Scholarship {name: 'Học bổng 2', description: 'Học bổng dành cho sinh viên có hoàn cảnh khó khăn tại Trường Đại học Sài Gòn.'})
MERGE (university)-[:hasScholarship]->(scholarship1)
MERGE (university)-[:hasScholarship]->(scholarship2)

MERGE (internationalPartner1:InternationalCooperation {name: 'Đối tác quốc tế 1', description: 'Đối tác hợp tác quốc tế của Trường Đại học Sài Gòn.'})
MERGE (internationalPartner2:InternationalCooperation {name: 'Đối tác quốc tế 2', description: 'Đối tác hợp tác quốc tế của Trường Đại học Sài Gòn.'})
MERGE (university)-[:hasInternationalCooperation]->(internationalPartner1)
MERGE (university)-[:hasInternationalCooperation]->(internationalPartner2)

MERGE (bachelorProgram:Program {name: 'Chương trình đại học', description: 'Chương trình đào tạo trình độ đại học tại Trường Đại học Sài Gòn.'})
MERGE (masterProgram:Program {name: 'Chương trình cao học', description: 'Chương trình đào tạo trình độ cao học tại Trường Đại học Sài Gòn.'})
MERGE (doctoralProgram:Program {name: 'Chương trình tiến sĩ', description: 'Chương trình đào tạo trình độ tiến sĩ tại Trường Đại học Sài Gòn.'})
MERGE (university)-[:offersProgram]->(bachelorProgram)
MERGE (university)-[:offersProgram]->(masterProgram)
MERGE (university)-[:offersProgram]->(doctoralProgram)

MERGE (majorField1:FieldOfStudy {name: 'Lĩnh vực 1', description: 'Lĩnh vực đào tạo chính tại Trường Đại học Sài Gòn.'})
MERGE (majorField2:FieldOfStudy {name: 'Lĩnh vực 2', description: 'Lĩnh vực đào tạo chính tại Trường Đại học Sài Gòn.'})
MERGE (majorField3:FieldOfStudy {name: 'Lĩnh vực 3', description: 'Lĩnh vực đào tạo chính tại Trường Đại học Sài Gòn.'})
MERGE (university)-[:hasFieldOfStudy]->(majorField1)
MERGE (university)-[:hasFieldOfStudy]->(majorField2)
MERGE (university)-[:hasFieldOfStudy]->(majorField3)
MERGE (university:University {name: 'Trường Đại học Sài Gòn', description: 'Cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo; là trường đại học đào tạo đa ngành, đa lĩnh vực. Trường Đại học Sài Gòn đào tạo từ trình độ đại học và sau đại học, theo 2 phương thức: chính quy và giáo dục thường xuyên (vừa làm vừa học, văn bằng hai, liên thông). Hiện nay, Trường đang tổ chức đào tạo 05 chuyên ngành tiến sĩ, 12 chuyên ngành cao học và 39 chương trình đào tạo trình độ đại học thuộc các lĩnh vực: Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm. Ngoài việc cấp bằng, Trường Đại học Sài Gòn được Bộ Giáo dục và Đào tạo cho phép đào tạo cấp các chứng chỉ Bồi dưỡng nghiệp vụ sư phạm cho giảng viên đại học, cao đẳng và bồi dưỡng nghiệp vụ sư phạm cho giáo viên Tiếng Anh Tiểu học, chứng chỉ Công nghệ Thông tin và chứng chỉ Tiếng Anh theo khung năng lực Ngoại ngữ 6 bậc dùng cho Việt Nam. Ngày 13/5/2017, Trường Đại học Sài Gòn được Chứng nhận kiểm định chất lượng giáo dục trường đại học. Năm 2018, Trường đón nhận Huân chương Lao động Hạng Ba do Chủ tịch nước Cộng hòa Xã hội Chủ nghĩa Việt Nam trao tặng.'})

MERGE (leadership:Department {name: 'Ban lãnh đạo', description: 'Ban lãnh đạo của Trường Đại học Sài Gòn bao gồm Đảng ủy, Hiệu trưởng, Các Phó Hiệu trưởng và Hội đồng trường.'})
MERGE (university)-[:hasDepartment]->(leadership)

MERGE (organizations:Department {name: 'Các tổ chức đoàn thể', description: 'Các tổ chức đoàn thể tại Trường Đại học Sài Gòn bao gồm Công đoàn, Đoàn Thanh niên và Hội Sinh viên.'})
MERGE (university)-[:hasDepartment]->(organizations)

MERGE (functionalDepartments:Department {name: 'Các phòng ban chức năng', description: 'Các phòng ban chức năng tại Trường Đại học Sài Gòn bao gồm Đào tạo, Tổ chức - Cán bộ, Văn phòng, Kế hoạch - Tài chính, Công tác sinh viên, Quản lý khoa học, Đào tạo sau đại học, Thanh tra - Pháp chế, Khảo thí & Đảm bảo chất lượng, Ban Quản lý Dự án & Xây dựng, Hợp tác quốc tế & Doanh nghiệp, Thiết bị, Giáo dục thường xuyên.'})
MERGE (university)-[:hasDepartment]->(functionalDepartments)

MERGE (centers:Department {name: 'Các trung tâm trực thuộc', description: 'Các trung tâm trực thuộc Trường Đại học Sài Gòn bao gồm Khảo thí, Đào tạo quốc tế, Hỗ trợ sinh viên, Học liệu, Công nghệ thông tin, Ngoại ngữ, Trung tâm Tuyển sinh & Truyền thông, Trung tâm Ký túc xá, Trạm Y tế.'})
MERGE (university)-[:hasDepartment]->(centers)

MERGE (faculties:Department {name: 'Các khoa chuyên môn', description: 'Các khoa chuyên môn tại Trường Đại học Sài Gòn bao gồm Giáo dục Mầm non, Giáo dục Tiểu học, Sư phạm Khoa học Xã hội, Sư phạm Khoa học Tự nhiên, Giáo dục, Nghệ thuật, Ngoại ngữ, Thư viện - Văn phòng, Khoa học Môi trường, Công nghệ Thông tin, Quản trị Kinh doanh, Tài chính - Kế toán, Văn hóa và Du lịch, Khoa học Chính trị, Toán - Ứng dụng, Điện tử - Viễn thông, Giáo dục Quốc phòng & An ninh - Giáo dục Thể chất.'})
MERGE (university)-[:hasDepartment]->(faculties)

MERGE (subUnits:Department {name: 'Đơn vị trực thuộc', description: 'Các đơn vị trực thuộc Trường Đại học Sài Gòn bao gồm Viện Khoa học Dữ liệu và Trí tuệ nhân tạo, Viện Nghiên cứu Môi trường - Sức khỏe, Trung tâm Thực hành Sư phạm, Trung học Thực hành Sài Gòn, Tiểu học Thực hành Sài Gòn.'})
MERGE (university)-[:hasDepartment]->(subUnits)
MERGE (university:University {name: 'Trường Đại học Sài Gòn', description: 'Cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo; là trường đại học đào tạo đa ngành, đa lĩnh vực. Trường Đại học Sài Gòn đào tạo từ trình độ đại học và sau đại học, theo 2 phương thức: chính quy và giáo dục thường xuyên (vừa làm vừa học, văn bằng hai, liên thông). Hiện nay, Trường đang tổ chức đào tạo 05 chuyên ngành tiến sĩ, 12 chuyên ngành cao học và 39 chương trình đào tạo trình độ đại học thuộc các lĩnh vực: Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm. Ngoài việc cấp bằng, Trường Đại học Sài Gòn được Bộ Giáo dục và Đào tạo cho phép đào tạo cấp các chứng chỉ Bồi dưỡng nghiệp vụ sư phạm cho giảng viên đại học, cao đẳng và bồi dưỡng nghiệp vụ sư phạm cho giáo viên Tiếng Anh Tiểu học, chứng chỉ Công nghệ Thông tin và chứng chỉ Tiếng Anh theo khung năng lực Ngoại ngữ 6 bậc dùng cho Việt Nam. Ngày 13/5/2017, Trường Đại học Sài Gòn được Chứng nhận kiểm định chất lượng giáo dục trường đại học. Năm 2018, Trường đón nhận Huân chương Lao động Hạng Ba do Chủ tịch nước Cộng hòa Xã hội Chủ nghĩa Việt Nam trao tặng.'})

MERGE (regularSystem:Program {name: 'Hệ chính quy', description: 'Chương trình đào tạo chính quy tại Trường Đại học Sài Gòn.'})
MERGE (university)-[:offersProgram]->(regularSystem)

MERGE (undergraduateDegree:Program {name: 'Trình độ Đại học', description: 'Chương trình đào tạo trình độ đại học tại Trường Đại học Sài Gòn.'})
MERGE (regularSystem)-[:offersProgram]->(undergraduateDegree)

MERGE (bachelorPrograms:Program {name: 'Chương trình đại trà', description: 'Chương trình đại trà tại Trường Đại học Sài Gòn bao gồm nhiều chuyên ngành khác nhau.'})
MERGE (undergraduateDegree)-[:offersProgram]->(bachelorPrograms)

MERGE (field1:FieldOfStudy {name: 'Giáo dục Chính trị - Du lịch', description: 'Chuyên ngành Giáo dục Chính trị - Du lịch.'})
MERGE (field2:FieldOfStudy {name: 'Giáo dục Mầm non - Kế toán', description: 'Chuyên ngành Giáo dục Mầm non - Kế toán.'})
MERGE (field3:FieldOfStudy {name: 'Giáo dục Tiểu học - Khoa học Môi trường', description: 'Chuyên ngành Giáo dục Tiểu học - Khoa học Môi trường.'})
MERGE (field4:FieldOfStudy {name: 'Sư phạm Âm nhạc - Kinh doanh Quốc tế', description: 'Chuyên ngành Sư phạm Âm nhạc - Kinh doanh Quốc tế.'})
MERGE (field5:FieldOfStudy {name: 'Sư phạm Địa lý - Kỹ thuật Điện', description: 'Chuyên ngành Sư phạm Địa lý - Kỹ thuật Điện.'})
MERGE (field6:FieldOfStudy {name: 'Sư phạm Hóa học - Kỹ thuật Điện tử - Viễn thông', description: 'Chuyên ngành Sư phạm Hóa học - Kỹ thuật Điện tử - Viễn thông.'})
MERGE (field7:FieldOfStudy {name: 'Sư phạm Khoa học Tự nhiên - Kỹ thuật Phần mềm', description: 'Chuyên ngành Sư phạm Khoa học Tự nhiên - Kỹ thuật Phần mềm.'})
MERGE (field8:FieldOfStudy {name: 'Sư phạm Lịch sử - Luật', description: 'Chuyên ngành Sư phạm Lịch sử - Luật.'})
MERGE (field9:FieldOfStudy {name: 'Sư phạm Lịch sử - Địa lý - Ngôn ngữ Anh', description: 'Chuyên ngành Sư phạm Lịch sử - Địa lý - Ngôn ngữ Anh.'})
MERGE (field10:FieldOfStudy {name: 'Sư phạm Mỹ thuật - Quản lý Giáo dục', description: 'Chuyên ngành Sư phạm Mỹ thuật - Quản lý Giáo dục.'})
MERGE (field11:FieldOfStudy {name: 'Sư phạm Ngữ Văn - Quản trị Kinh doanh', description: 'Chuyên ngành Sư phạm Ngữ Văn - Quản trị Kinh doanh.'})
MERGE (field12:FieldOfStudy {name: 'Sư phạm Sinh học - Quản trị Văn phòng', description: 'Chuyên ngành Sư phạm Sinh học - Quản trị Văn phòng.'})
MERGE (field13:FieldOfStudy {name: 'Sư phạm Tiếng Anh - Quốc tế học', description: 'Chuyên ngành Sư phạm Tiếng Anh - Quốc tế học.'})
MERGE (field14:FieldOfStudy {name: 'Sư phạm Toán học - Tài chính - Ngân hàng', description: 'Chuyên ngành Sư phạm Toán học - Tài chính - Ngân hàng.'})
MERGE (field15:FieldOfStudy {name: 'Sư phạm Vật lý - Tâm lý học', description: 'Chuyên ngành Sư phạm Vật lý - Tâm lý học.'})
MERGE (field16:FieldOfStudy {name: 'CNKT Điện tử - Viễn thông - Thanh nhạc', description: 'Chuyên ngành CNKT Điện tử - Viễn thông - Thanh nhạc.'})
MERGE (field17:FieldOfStudy {name: 'CNKT Điện, Điện tử - Thông tin - Thư viện', description: 'Chuyên ngành CNKT Điện, Điện tử - Thông tin - Thư viện.'})
MERGE (field18:FieldOfStudy {name: 'Công nghệ Kỹ thuật Môi trường - Toán Ứng dụng', description: 'Chuyên ngành Công nghệ Kỹ thuật Môi trường - Toán Ứng dụng.'})
MERGE (field19:FieldOfStudy {name: 'Công nghệ Thông tin - Việt Nam học', description: 'Chuyên ngành Công nghệ Thông tin - Việt Nam học.'})

MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field1)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field2)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field3)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field4)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field5)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field6)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field7)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field8)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field9)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field10)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field11)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field12)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field13)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field14)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field15)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field16)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field17)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field18)
MERGE (bachelorPrograms)-[:hasFieldOfStudy]->(field19)

MERGE (highQualityProgram:Program {name: 'Chương trình chất lượng cao', description: 'Chương trình chất lượng cao tại Trường Đại học Sài Gòn, chuyên ngành Công nghệ Thông tin.'})
MERGE (undergraduateDegree)-[:offersProgram]->(highQualityProgram)

MERGE (postgraduateDegree:Program {name: 'Trình độ Sau Đại học', description: 'Chương trình đào tạo trình độ sau đại học tại Trường Đại học Sài Gòn.'})
MERGE (regularSystem)-[:offersProgram]->(postgraduateDegree)

MERGE (postgraduateField1:FieldOfStudy {name: 'Hóa hữu cơ', description: 'Chuyên ngành Hóa hữu cơ.'})
MERGE (postgraduateField2:FieldOfStudy {name: 'Quản trị Kinh doanh', description: 'Chuyên ngành Quản trị Kinh doanh.'})
MERGE (postgraduateField3:FieldOfStudy {name: 'Hóa lý thuyết và Hóa lý', description: 'Chuyên ngành Hóa lý thuyết và Hóa lý.'})
MERGE (postgraduateField4:FieldOfStudy {name: 'Tài chính – Ngân hàng', description: 'Chuyên ngành Tài chính – Ngân hàng.'})
MERGE (postgraduateField5:FieldOfStudy {name: 'Khoa học Máy tính', description: 'Chuyên ngành Khoa học Máy tính.'})
MERGE (postgraduateField6:FieldOfStudy {name: 'Toán Giải tích', description: 'Chuyên ngành Toán Giải tích.'})
MERGE (postgraduateField7:FieldOfStudy {name: 'Lịch sử Việt Nam', description: 'Chuyên ngành Lịch sử Việt Nam.'})
MERGE (postgraduateField8:FieldOfStudy {name: 'Văn học Việt Nam', description: 'Chuyên ngành Văn học Việt Nam.'})
MERGE (postgraduateField9:FieldOfStudy {name: 'LL & PPDH bộ môn Toán', description: 'Chuyên ngành LL & PPDH bộ môn Toán.'})
MERGE (postgraduateField10:FieldOfStudy {name: 'Luật dân sự và tố tụng dân sự', description: 'Chuyên ngành Luật dân sự và tố tụng dân sự.'})
MERGE (postgraduateField11:FieldOfStudy {name: 'Ngôn ngữ học', description: 'Chuyên ngành Ngôn ngữ học.'})
MERGE (postgraduateField12:FieldOfStudy {name: 'Quản lý Giáo dục', description: 'Chuyên ngành Quản lý Giáo dục.'})

MERGE (postgraduateDegree)-[:hasFieldOfStudy]->(postgraduateField1)
MERGE (postgraduateDegree)-[:hasFieldOfStudy]->(postgraduateField2)
MERGE (postgraduateDegree)-[:hasFieldOfStudy]->(postgraduateField3)
MERGE (postgraduateDegree)-[:hasFieldOfStudy]->(postgraduateField4)
MERGE (postgraduateDegree)-[:hasFieldOfStudy]->(postgraduateField5)
MERGE (postgraduateDegree)-[:hasFieldOfStudy]->(postgraduateField6)
MERGE (postgraduateDegree)-[:hasFieldOfStudy]->(postgraduateField7)
MERGE (postgraduateDegree)-[:hasFieldOfStudy]->(postgraduateField8)
MERGE (postgraduateDegree)-[:hasFieldOfStudy]->(postgraduateField9)
MERGE (postgraduateDegree)-[:hasFieldOfStudy]->(postgraduateField10)
MERGE (postgraduateDegree)-[:hasFieldOfStudy]->(postgraduateField11)
MERGE (postgraduateDegree)-[:hasFieldOfStudy]->(postgraduateField12)

MERGE (doctoralDegree:Program {name: 'Trình độ Tiến sĩ', description: 'Chương trình đào tạo trình độ tiến sĩ tại Trường Đại học Sài Gòn.'})
MERGE (regularSystem)-[:offersProgram]->(doctoralDegree)

MERGE (doctoralField1:FieldOfStudy {name: 'Hóa hữu cơ', description: 'Chuyên ngành Hóa hữu cơ.'})
MERGE (doctoralField2:FieldOfStudy {name: 'Lịch sử Việt Nam', description: 'Chuyên ngành Lịch sử Việt Nam.'})
MERGE (doctoralField3:FieldOfStudy {name: 'Quản lý Giáo dục', description: 'Chuyên ngành Quản lý Giáo dục.'})
MERGE (doctoralField4:FieldOfStudy {name: 'Toán Giải tích', description: 'Chuyên ngành Toán Giải tích.'})
MERGE (doctoralField5:FieldOfStudy {name: 'Quản trị Kinh doanh', description: 'Chuyên ngành Quản trị Kinh doanh.'})

MERGE (doctoralDegree)-[:hasFieldOfStudy]->(doctoralField1)
MERGE (doctoralDegree)-[:hasFieldOfStudy]->(doctoralField2)
MERGE (doctoralDegree)-[:hasFieldOfStudy]->(doctoralField3)
MERGE (doctoralDegree)-[:hasFieldOfStudy]->(doctoralField4)
MERGE (doctoralDegree)-[:hasFieldOfStudy]->(doctoralField5)

MERGE (continuingEducation:Program {name: 'Giáo dục thường xuyên', description: 'Chương trình giáo dục thường xuyên tại Trường Đại học Sài Gòn.'})
MERGE (university)-[:offersProgram]->(continuingEducation)

MERGE (continuingField1:FieldOfStudy {name: 'Công nghệ Thông tin', description: 'Chuyên ngành Công nghệ Thông tin trong chương trình giáo dục thường xuyên.'})
MERGE (continuingField2:FieldOfStudy {name: 'Kế toán', description: 'Chuyên ngành Kế toán trong chương trình giáo dục thường xuyên.'})
MERGE (continuingField3:FieldOfStudy {name: 'Quản trị Kinh doanh', description: 'Chuyên ngành Quản trị Kinh doanh trong chương trình giáo dục thường xuyên.'})
MERGE (continuingField4:FieldOfStudy {name: 'Giáo dục Mầm non', description: 'Chuyên ngành Giáo dục Mầm non trong chương trình giáo dục thường xuyên.'})
MERGE (continuingField5:FieldOfStudy {name: 'Giáo dục Tiểu học', description: 'Chuyên ngành Giáo dục Tiểu học trong chương trình giáo dục thường xuyên.'})

MERGE (continuingEducation)-[:hasFieldOfStudy]->(continuingField1)
MERGE (continuingEducation)-[:hasFieldOfStudy]->(continuingField2)
MERGE (continuingEducation)-[:hasFieldOfStudy]->(continuingField3)
MERGE (continuingEducation)-[:hasFieldOfStudy]->(continuingField4)
MERGE (continuingEducation)-[:hasFieldOfStudy]->(continuingField5)
MERGE (university:University {name: 'Trường Đại học Sài Gòn', description: 'Cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo; là trường đại học đào tạo đa ngành, đa lĩnh vực. Trường Đại học Sài Gòn đào tạo từ trình độ đại học và sau đại học, theo 2 phương thức: chính quy và giáo dục thường xuyên (vừa làm vừa học, văn bằng hai, liên thông). Hiện nay, Trường đang tổ chức đào tạo 05 chuyên ngành tiến sĩ, 12 chuyên ngành cao học và 39 chương trình đào tạo trình độ đại học thuộc các lĩnh vực: Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm. Ngoài việc cấp bằng, Trường Đại học Sài Gòn được Bộ Giáo dục và Đào tạo cho phép đào tạo cấp các chứng chỉ Bồi dưỡng nghiệp vụ sư phạm cho giảng viên đại học, cao đẳng và bồi dưỡng nghiệp vụ sư phạm cho giáo viên Tiếng Anh Tiểu học, chứng chỉ Công nghệ Thông tin và chứng chỉ Tiếng Anh theo khung năng lực Ngoại ngữ 6 bậc dùng cho Việt Nam. Ngày 13/5/2017, Trường Đại học Sài Gòn được Chứng nhận kiểm định chất lượng giáo dục trường đại học. Năm 2018, Trường đón nhận Huân chương Lao động Hạng Ba do Chủ tịch nước Cộng hòa Xã hội Chủ nghĩa Việt Nam trao tặng.'})

MERGE (internationalCooperation:InternationalCooperation {name: 'Công tác đối ngoại', description: 'Hoạt động hợp tác quốc tế tại Trường Đại học Sài Gòn, duy trì và thiết lập mối quan hệ hợp tác với các trường Đại học nước ngoài và các tổ chức quốc tế.'})
MERGE (university)-[:hasInternationalCooperation]->(internationalCooperation)

MERGE (program1:Program {name: 'Chương trình Cử nhân Quốc tế Quản trị Kinh doanh và Quản lý Thương mại Điện tử', description: 'Chương trình liên kết đào tạo giữa Trường Đại học Sài Gòn và trường Đại học Khoa học Ứng dụng IMC Krems (Cộng hòa Áo).'})
MERGE (internationalCooperation)-[:offersProgram]->(program1)

MERGE (program2:Program {name: 'Chương trình đào tạo tiếng Hoa', description: 'Chương trình liên kết với Hiệp hội Phát triển Kinh tế Văn hóa Giáo dục Đài Việt, bao gồm Hoa ngữ giao tiếp, Luyện thi TOCFL, Hoa ngữ lớp Online.'})
MERGE (internationalCooperation)-[:offersProgram]->(program2)

MERGE (scholarship1:Scholarship {name: 'Học bổng toàn phần của Bộ Y tế Singapore', description: 'Chương trình học bổng toàn phần cho sinh viên đào tạo Trợ lý bác sĩ với trị giá SGD 120,000 từ Tập đoàn Y tế Quốc gia Singapore.'})
MERGE (internationalCooperation)-[:hasScholarship]->(scholarship1)

MERGE (scholarship2:Scholarship {name: 'Học bổng của Bộ Giáo dục Đài Loan', description: 'Học bổng Cử nhân hệ chính quy, vừa học vừa làm đối với các Khối ngành Kinh tế, Thương mại, Thực phẩm, Dịch vụ, Công nghệ Thông tin, Kỹ thuật.'})
MERGE (internationalCooperation)-[:hasScholarship]->(scholarship2)

MERGE (program3:Program {name: 'Chương trình liên kết đào tạo khác', description: 'Ký kết hợp tác và xây dựng chương trình chuyển tiếp các ngành Công nghệ thông tin, Ngôn ngữ Anh, Sư phạm Anh, Quản trị kinh doanh, Tài chính - Ngân hàng thuộc Đại học Huddersfiled.'})
MERGE (internationalCooperation)-[:offersProgram]->(program3)
MERGE (university:University {name: 'Trường Đại học Sài Gòn', description: 'Cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo; là trường đại học đào tạo đa ngành, đa lĩnh vực. Trường Đại học Sài Gòn đào tạo từ trình độ đại học và sau đại học, theo 2 phương thức: chính quy và giáo dục thường xuyên (vừa làm vừa học, văn bằng hai, liên thông). Hiện nay, Trường đang tổ chức đào tạo 05 chuyên ngành tiến sĩ, 12 chuyên ngành cao học và 39 chương trình đào tạo trình độ đại học thuộc các lĩnh vực: Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm. Ngoài việc cấp bằng, Trường Đại học Sài Gòn được Bộ Giáo dục và Đào tạo cho phép đào tạo cấp các chứng chỉ Bồi dưỡng nghiệp vụ sư phạm cho giảng viên đại học, cao đẳng và bồi dưỡng nghiệp vụ sư phạm cho giáo viên Tiếng Anh Tiểu học, chứng chỉ Công nghệ Thông tin và chứng chỉ Tiếng Anh theo khung năng lực Ngoại ngữ 6 bậc dùng cho Việt Nam. Ngày 13/5/2017, Trường Đại học Sài Gòn được Chứng nhận kiểm định chất lượng giáo dục trường đại học. Năm 2018, Trường đón nhận Huân chương Lao động Hạng Ba do Chủ tịch nước Cộng hòa Xã hội Chủ nghĩa Việt Nam trao tặng.'})

MERGE (researchTopic:Research {name: 'Đề tài Nghiên cứu khoa học cấp cơ sở', description: 'Sinh viên tham gia thực hiện đề tài NCKH trong thời gian từ 06 – 09 tháng dưới sự hướng dẫn của Giảng viên.'})
MERGE (university)-[:offersProgram]->(researchTopic)

MERGE (researchBenefits:Research {name: 'Quyền lợi NCKH', description: 'Đối với các đề tài có kết quả nghiệm thu đạt trở lên sẽ được hỗ trợ kinh phí, cộng điểm rèn luyện năm học và cấp giấy chứng nhận NCKH.'})
MERGE (university)-[:offersProgram]->(researchBenefits)

MERGE (scientificPaper:Research {name: 'Bài báo Khoa học và báo cáo tham luận Hội thảo', description: 'Sinh viên có bài báo đăng trên các Tạp chí chuyên ngành trong nước, quốc tế hoặc báo cáo khoa học đăng trên kỷ yếu các Hội thảo/Hội nghị chuyên ngành cấp quốc gia, quốc tế.'})
MERGE (university)-[:offersProgram]->(scientificPaper)

MERGE (researchRegulations:Research {name: 'Quy chế quản lý hoạt động Khoa học và Công nghệ', description: 'Thông tin chi tiết về NCKH, sinh viên xem tại Chương 7, Quy chế quản lý hoạt động Khoa học và Công nghệ Trường ĐHSG.'})
MERGE (university)-[:offersProgram]->(researchRegulations)
MERGE (university:University {name: 'Trường Đại học Sài Gòn', description: 'Cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo; là trường đại học đào tạo đa ngành, đa lĩnh vực. Trường Đại học Sài Gòn đào tạo từ trình độ đại học và sau đại học, theo 2 phương thức: chính quy và giáo dục thường xuyên (vừa làm vừa học, văn bằng hai, liên thông). Hiện nay, Trường đang tổ chức đào tạo 05 chuyên ngành tiến sĩ, 12 chuyên ngành cao học và 39 chương trình đào tạo trình độ đại học thuộc các lĩnh vực: Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm. Ngoài việc cấp bằng, Trường Đại học Sài Gòn được Bộ Giáo dục và Đào tạo cho phép đào tạo cấp các chứng chỉ Bồi dưỡng nghiệp vụ sư phạm cho giảng viên đại học, cao đẳng và bồi dưỡng nghiệp vụ sư phạm cho giáo viên Tiếng Anh Tiểu học, chứng chỉ Công nghệ Thông tin và chứng chỉ Tiếng Anh theo khung năng lực Ngoại ngữ 6 bậc dùng cho Việt Nam. Ngày 13/5/2017, Trường Đại học Sài Gòn được Chứng nhận kiểm định chất lượng giáo dục trường đại học. Năm 2018, Trường đón nhận Huân chương Lao động Hạng Ba do Chủ tịch nước Cộng hòa Xã hội Chủ nghĩa Việt Nam trao tặng.'})

MERGE (journal:Journal {name: 'Tạp chí Khoa học Đại học Sài Gòn', description: 'Tạp chí Khoa học phục vụ cán bộ giảng dạy, nghiên cứu, quản lý, sinh viên các trường đại học, cao đẳng, các viện, học viện, các trung tâm nghiên cứu.'})
MERGE (university)-[:publishesIn]->(journal)

MERGE (journalInfo:Research {name: 'Giới thiệu chung về tạp chí Khoa học Đại học Sài Gòn', description: 'Tên cơ quan chủ quản: Trường Đại học Sài Gòn. Tên cơ quan báo chí: Tạp chí Khoa học Đại học Sài Gòn. Đối tượng phục vụ: Cán bộ giảng dạy, nghiên cứu, quản lý, sinh viên các trường đại học, cao đẳng, các viện, học viện, các trung tâm nghiên cứu.'})
MERGE (journal)-[:hasFieldOfStudy]->(journalInfo)

MERGE (journalPurpose:Research {name: 'Tôn chỉ, mục đích hoạt động báo chí', description: 'Là diễn đàn khoa học công bố các kết quả nghiên cứu và hoạt động khoa học của cán bộ, giảng viên trường Đại học Sài Gòn. Là diễn đàn trao đổi kinh nghiệm về giảng dạy, học tập của giáo viên và sinh viên.'})
MERGE (journal)-[:hasFieldOfStudy]->(journalPurpose)

MERGE (journalLocation:Research {name: 'Trụ sở Toà soạn', description: 'Địa chỉ: 273 An Dương Vương, Phường 3, Quận 5, TP. Hồ Chí Minh. Điện thoại: (028) 38 321 360. Email: tcdhsg@sgu.edu.vn. Website: http://sj.sgu.edu.vn/'})
MERGE (journal)-[:hasFieldOfStudy]->(journalLocation)

MERGE (journalRegulations:Research {name: 'Quy định chung về bài báo khoa học', description: 'Phải nêu rõ mục tiêu nghiên cứu; cần có các kết quả mới, có giá trị khoa học và thực tiễn trong lĩnh vực nghiên cứu; phải được phản biện và phải có danh mục chú thích và tài liệu tham khảo.'})
MERGE (journal)-[:hasFieldOfStudy]->(journalRegulations)

MERGE (submissionGuidelines:Research {name: 'Thể lệ gửi bài đăng tạp chí Khoa học Đại Học Sài Gòn', description: 'Bài gửi đăng trên Tạp chí phải là công trình khoa học, các báo cáo học thuật hoặc kết quả thực hiện đề tài khoa học mới của tác giả trong và ngoài nước, có giá trị khoa học và thực tiễn, chưa từng công bố trong ấn phẩm khác.'})
MERGE (journal)-[:hasFieldOfStudy]->(submissionGuidelines)