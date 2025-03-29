cypher
MATCH (u:University {name: 'Trường Đại học Sài Gòn'})
WITH u
MERGE (ic_general:InternationalCooperation {name: 'Hợp tác quốc tế đa phương'})
ON CREATE SET ic_general.description = 'Hoạt động hợp tác quốc tế chung của Trường Đại học Sài Gòn với các trường đại học và tổ chức quốc tế ở nhiều nước như Hoa Kỳ, Anh, Nga, Pháp, Australia, Trung Quốc, Singapore, Malaysia, Cộng hòa Áo, New Zealand, Thụy Điển, nhằm thực hiện dự án đào tạo, nghiên cứu khoa học và trao đổi học thuật.'
ON MATCH SET ic_general.description = 'Hoạt động hợp tác quốc tế chung của Trường Đại học Sài Gòn với các trường đại học và tổ chức quốc tế ở nhiều nước như Hoa Kỳ, Anh, Nga, Pháp, Australia, Trung Quốc, Singapore, Malaysia, Cộng hòa Áo, New Zealand, Thụy Điển, nhằm thực hiện dự án đào tạo, nghiên cứu khoa học và trao đổi học thuật.'
MERGE (u)-[:hasInternationalCooperation]->(ic_general)
WITH u
MERGE (ic_krems:InternationalCooperation {name: 'Trường Đại học Khoa học Ứng dụng IMC Krems'})
ON CREATE SET ic_krems.description = 'Trường Đại học Khoa học Ứng dụng IMC Krems (Cộng hòa Áo), đối tác liên kết đào tạo với Trường Đại học Sài Gòn trong chương trình Cử nhân Quốc tế Quản trị Kinh doanh và Quản lý Thương mại Điện tử.'
ON MATCH SET ic_krems.description = 'Trường Đại học Khoa học Ứng dụng IMC Krems (Cộng hòa Áo), đối tác liên kết đào tạo với Trường Đại học Sài Gòn trong chương trình Cử nhân Quốc tế Quản trị Kinh doanh và Quản lý Thương mại Điện tử.'
MERGE (u)-[:hasInternationalCooperation]->(ic_krems)
WITH u
MERGE (p_krems:Program {name: 'Chương trình Cử nhân Quốc tế Quản trị Kinh doanh và Quản lý Thương mại Điện tử'})
ON CREATE SET p_krems.description = 'Chương trình liên kết đào tạo cấp bằng Cử nhân giữa Trường Đại học Sài Gòn và Trường Đại học Khoa học Ứng dụng IMC Krems (Cộng hòa Áo), được Bộ Giáo dục và Đào tạo phê duyệt theo Quyết định số 1498/QĐ-BGDĐT ngày 28/4/2014.'
ON MATCH SET p_krems.description = 'Chương trình liên kết đào tạo cấp bằng Cử nhân giữa Trường Đại học Sài Gòn và Trường Đại học Khoa học Ứng dụng IMC Krems (Cộng hòa Áo), được Bộ Giáo dục và Đào tạo phê duyệt theo Quyết định số 1498/QĐ-BGDĐT ngày 28/4/2014.'
MERGE (u)-[:offersProgram]->(p_krems)
WITH u
MERGE (ic_daiviet:InternationalCooperation {name: 'Hiệp hội Phát triển Kinh tế Văn hóa Giáo dục Đài Việt'})
ON CREATE SET ic_daiviet.description = 'Hiệp hội Phát triển Kinh tế Văn hóa Giáo dục Đài Việt, đối tác liên kết với Trường Đại học Sài Gòn trong chương trình đào tạo tiếng Hoa (Đài Loan).'
ON MATCH SET ic_daiviet.description = 'Hiệp hội Phát triển Kinh tế Văn hóa Giáo dục Đài Việt, đối tác liên kết với Trường Đại học Sài Gòn trong chương trình đào tạo tiếng Hoa (Đài Loan).'
MERGE (u)-[:hasInternationalCooperation]->(ic_daiviet)
WITH u
MERGE (p_hoa:Program {name: 'Chương trình đào tạo tiếng Hoa (Đài Loan)'})
ON CREATE SET p_hoa.description = 'Chương trình liên kết đào tạo tiếng Hoa (Đài Loan) giữa Trường Đại học Sài Gòn và Hiệp hội Phát triển Kinh tế Văn hóa Giáo dục Đài Việt. Bao gồm các nội dung: Hoa ngữ giao tiếp, Luyện thi TOCFL, Hoa ngữ lớp Online. Chứng chỉ được cấp bởi Trung tâm Hoa Ngữ Sư Phạm Đài Loan (Đại học Quốc gia Sư Phạm Đài Loan).'
ON MATCH SET p_hoa.description = 'Chương trình liên kết đào tạo tiếng Hoa (Đài Loan) giữa Trường Đại học Sài Gòn và Hiệp hội Phát triển Kinh tế Văn hóa Giáo dục Đài Việt. Bao gồm các nội dung: Hoa ngữ giao tiếp, Luyện thi TOCFL, Hoa ngữ lớp Online. Chứng chỉ được cấp bởi Trung tâm Hoa Ngữ Sư Phạm Đài Loan (Đại học Quốc gia Sư Phạm Đài Loan).'
MERGE (u)-[:offersProgram]->(p_hoa)
WITH u
MERGE (ic_singapore:InternationalCooperation {name: 'Bộ Y tế Singapore (MOHH)'})
ON CREATE SET ic_singapore.description = 'Bộ Y tế Singapore (thông qua Tập đoàn Y tế Quốc gia MOHH), đơn vị cung cấp Học bổng toàn phần Asian Nursing Scholarship cho sinh viên Trường Đại học Sài Gòn.'
ON MATCH SET ic_singapore.description = 'Bộ Y tế Singapore (thông qua Tập đoàn Y tế Quốc gia MOHH), đơn vị cung cấp Học bổng toàn phần Asian Nursing Scholarship cho sinh viên Trường Đại học Sài Gòn.'
MERGE (u)-[:hasInternationalCooperation]->(ic_singapore)
WITH u
MERGE (p_ans:Program {name: 'Học bổng Asian Nursing Scholarship (Singapore)'})
ON CREATE SET p_ans.description = 'Chương trình Học bổng toàn phần của Bộ Y tế Singapore (MOHH) dành cho sinh viên Trường Đại học Sài Gòn để đào tạo Trợ lý bác sĩ tại Singapore trong 3 năm. Bao gồm trợ cấp sinh hoạt phí, hỗ trợ ký túc xá, chi phí đi lại, dịch vụ y tế và cơ hội việc làm tại các bệnh viện hàng đầu Singapore sau tốt nghiệp.'
ON MATCH SET p_ans.description = 'Chương trình Học bổng toàn phần của Bộ Y tế Singapore (MOHH) dành cho sinh viên Trường Đại học Sài Gòn để đào tạo Trợ lý bác sĩ tại Singapore trong 3 năm. Bao gồm trợ cấp sinh hoạt phí, hỗ trợ ký túc xá, chi phí đi lại, dịch vụ y tế và cơ hội việc làm tại các bệnh viện hàng đầu Singapore sau tốt nghiệp.'
MERGE (u)-[:offersProgram]->(p_ans)
WITH u
MERGE (ic_taiwan_edu:InternationalCooperation {name: 'Bộ Giáo dục Đài Loan'})
ON CREATE SET ic_taiwan_edu.description = 'Bộ Giáo dục Đài Loan, đơn vị cung cấp học bổng Cử nhân hệ chính quy và hệ vừa học vừa làm cho sinh viên Trường Đại học Sài Gòn du học tại Đài Loan.'
ON MATCH SET ic_taiwan_edu.description = 'Bộ Giáo dục Đài Loan, đơn vị cung cấp học bổng Cử nhân hệ chính quy và hệ vừa học vừa làm cho sinh viên Trường Đại học Sài Gòn du học tại Đài Loan.'
MERGE (u)-[:hasInternationalCooperation]->(ic_taiwan_edu)
WITH u
MERGE (p_taiwan_scholarship:Program {name: 'Học bổng Bộ Giáo dục Đài Loan'})
ON CREATE SET p_taiwan_scholarship.description = 'Chương trình học bổng của Bộ Giáo dục Đài Loan và các trường Đại học tại Đài Loan dành cho sinh viên Trường Đại học Sài Gòn. Bao gồm học bổng Cử nhân hệ chính quy, vừa học vừa làm các khối ngành Kinh tế, Thương mại, Thực phẩm, Dịch vụ, Công nghệ Thông tin, Kỹ thuật. Hỗ trợ miễn giảm học phí, phí ký túc xá, thực tập có lương và hỗ trợ tìm việc làm sau tốt nghiệp.'
ON MATCH SET p_taiwan_scholarship.description = 'Chương trình học bổng của Bộ Giáo dục Đài Loan và các trường Đại học tại Đài Loan dành cho sinh viên Trường Đại học Sài Gòn. Bao gồm học bổng Cử nhân hệ chính quy, vừa học vừa làm các khối ngành Kinh tế, Thương mại, Thực phẩm, Dịch vụ, Công nghệ Thông tin, Kỹ thuật. Hỗ trợ miễn giảm học phí, phí ký túc xá, thực tập có lương và hỗ trợ tìm việc làm sau tốt nghiệp.'
MERGE (u)-[:offersProgram]->(p_taiwan_scholarship)
WITH u
MERGE (ic_huddersfield:InternationalCooperation {name: 'Đại học Huddersfiled'})
ON CREATE SET ic_huddersfield.description = 'Đại học Huddersfiled (Vương quốc Anh), đối tác hợp tác với Trường Đại học Sài Gòn trong việc xây dựng chương trình chuyển tiếp và liên kết đào tạo Thạc sĩ.'
ON MATCH SET ic_huddersfield.description = 'Đại học Huddersfiled (Vương quốc Anh), đối tác hợp tác với Trường Đại học Sài Gòn trong việc xây dựng chương trình chuyển tiếp và liên kết đào tạo Thạc sĩ.'
MERGE (u)-[:hasInternationalCooperation]->(ic_huddersfield)
WITH u
MERGE (p_huddersfield_transfer:Program {name: 'Chương trình chuyển tiếp (Đại học Huddersfiled)'})
ON CREATE SET p_huddersfield_transfer.description = 'Chương trình hợp tác chuyển tiếp giữa Trường Đại học Sài Gòn và Đại học Huddersfiled (Vương quốc Anh) cho các ngành Công nghệ thông tin, Ngôn ngữ Anh, Sư phạm Anh, Quản trị kinh doanh, Tài chính - Ngân hàng.'
ON MATCH SET p_huddersfield_transfer.description = 'Chương trình hợp tác chuyển tiếp giữa Trường Đại học Sài Gòn và Đại học Huddersfiled (Vương quốc Anh) cho các ngành Công nghệ thông tin, Ngôn ngữ Anh, Sư phạm Anh, Quản trị kinh doanh, Tài chính - Ngân hàng.'
MERGE (u)-[:offersProgram]->(p_huddersfield_transfer)
WITH u
MERGE (p_huddersfield_tesol:Program {name: 'Chương trình Thạc sĩ Giảng dạy tiếng Anh (TESOL - Đại học Huddersfiled)'})
ON CREATE SET p_huddersfield_tesol.description = 'Chương trình liên kết đào tạo Thạc sĩ Giảng dạy tiếng Anh (Master of TESOL) dự kiến triển khai giữa Trường Đại học Sài Gòn và Đại học Huddersfiled (Vương quốc Anh).'
ON MATCH SET p_huddersfield_tesol.description = 'Chương trình liên kết đào tạo Thạc sĩ Giảng dạy tiếng Anh (Master of TESOL) dự kiến triển khai giữa Trường Đại học Sài Gòn và Đại học Huddersfiled (Vương quốc Anh).'
MERGE (u)-[:offersProgram]->(p_huddersfield_tesol)
WITH u
MERGE (r_forum:Research {name: 'Diễn đàn giáo dục đại học, khoa học và nghiên cứu'})
ON CREATE SET r_forum.description = 'Hoạt động khoa học và nghiên cứu do Trường Đại học Sài Gòn phối hợp với Bộ Khoa học và Công nghệ, Bộ Giáo dục và Đào tạo Việt Nam, các trường Đại học, các tổ chức quốc tế tổ chức, thu hút sự tham gia của nhiều nhà khoa học, nhà quản lý trong và ngoài nước.'
ON MATCH SET r_forum.description = 'Hoạt động khoa học và nghiên cứu do Trường Đại học Sài Gòn phối hợp với Bộ Khoa học và Công nghệ, Bộ Giáo dục và Đào tạo Việt Nam, các trường Đại học, các tổ chức quốc tế tổ chức, thu hút sự tham gia của nhiều nhà khoa học, nhà quản lý trong và ngoài nước.'
MERGE (u)-[:conductsResearch]->(r_forum)