cypher
MATCH (u:University {name: 'Trường Đại học Sài Gòn'})
WITH u
MERGE (d1:Department {name: 'Đảng ủy'})
ON CREATE SET d1.description = 'Tổ chức lãnh đạo chính trị tại Trường Đại học Sài Gòn, định hướng và giám sát các hoạt động theo đường lối của Đảng.'
ON MATCH SET d1.description = 'Tổ chức lãnh đạo chính trị tại Trường Đại học Sài Gòn, định hướng và giám sát các hoạt động theo đường lối của Đảng.'
MERGE (u)-[:hasDepartment]->(d1)
WITH u
MERGE (d2:Department {name: 'Hiệu trưởng'})
ON CREATE SET d2.description = 'Người đứng đầu, chịu trách nhiệm quản lý và điều hành toàn bộ hoạt động của Trường Đại học Sài Gòn.'
ON MATCH SET d2.description = 'Người đứng đầu, chịu trách nhiệm quản lý và điều hành toàn bộ hoạt động của Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d2)
WITH u
MERGE (d3:Department {name: 'Các Phó Hiệu trưởng'})
ON CREATE SET d3.description = 'Giúp việc cho Hiệu trưởng, phụ trách các mảng công tác cụ thể theo sự phân công trong quản lý Trường Đại học Sài Gòn.'
ON MATCH SET d3.description = 'Giúp việc cho Hiệu trưởng, phụ trách các mảng công tác cụ thể theo sự phân công trong quản lý Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d3)
WITH u
MERGE (d4:Department {name: 'Hội đồng trường'})
ON CREATE SET d4.description = 'Tổ chức quản trị, đại diện quyền sở hữu của nhà trường, có chức năng quyết nghị về chiến lược, quy hoạch, kế hoạch phát triển của Trường Đại học Sài Gòn.'
ON MATCH SET d4.description = 'Tổ chức quản trị, đại diện quyền sở hữu của nhà trường, có chức năng quyết nghị về chiến lược, quy hoạch, kế hoạch phát triển của Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d4)
WITH u
MERGE (d5:Department {name: 'Công đoàn'})
ON CREATE SET d5.description = 'Tổ chức đại diện cho quyền và lợi ích hợp pháp, chính đáng của cán bộ, viên chức, người lao động tại Trường Đại học Sài Gòn.'
ON MATCH SET d5.description = 'Tổ chức đại diện cho quyền và lợi ích hợp pháp, chính đáng của cán bộ, viên chức, người lao động tại Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d5)
WITH u
MERGE (d6:Department {name: 'Đoàn Thanh niên'})
ON CREATE SET d6.description = 'Tổ chức chính trị - xã hội của thanh niên Việt Nam tại Trường Đại học Sài Gòn, thực hiện công tác giáo dục, rèn luyện đoàn viên, sinh viên.'
ON MATCH SET d6.description = 'Tổ chức chính trị - xã hội của thanh niên Việt Nam tại Trường Đại học Sài Gòn, thực hiện công tác giáo dục, rèn luyện đoàn viên, sinh viên.'
MERGE (u)-[:hasDepartment]->(d6)
WITH u
MERGE (d7:Department {name: 'Hội Sinh viên'})
ON CREATE SET d7.description = 'Tổ chức đại diện cho sinh viên Trường Đại học Sài Gòn, chăm lo đời sống vật chất, tinh thần và bảo vệ quyền lợi hợp pháp của sinh viên.'
ON MATCH SET d7.description = 'Tổ chức đại diện cho sinh viên Trường Đại học Sài Gòn, chăm lo đời sống vật chất, tinh thần và bảo vệ quyền lợi hợp pháp của sinh viên.'
MERGE (u)-[:hasDepartment]->(d7)
WITH u
MERGE (d8:Department {name: 'Phòng Đào tạo'})
ON CREATE SET d8.description = 'Phòng ban chức năng chịu trách nhiệm quản lý, tổ chức và giám sát công tác đào tạo trình độ đại học hệ chính quy tại Trường Đại học Sài Gòn.'
ON MATCH SET d8.description = 'Phòng ban chức năng chịu trách nhiệm quản lý, tổ chức và giám sát công tác đào tạo trình độ đại học hệ chính quy tại Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d8)
WITH u
MERGE (d9:Department {name: 'Phòng Tổ chức - Cán bộ'})
ON CREATE SET d9.description = 'Phòng ban chức năng tham mưu và thực hiện công tác tổ chức bộ máy, quản lý nhân sự, cán bộ, viên chức tại Trường Đại học Sài Gòn.'
ON MATCH SET d9.description = 'Phòng ban chức năng tham mưu và thực hiện công tác tổ chức bộ máy, quản lý nhân sự, cán bộ, viên chức tại Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d9)
WITH u
MERGE (d10:Department {name: 'Văn phòng'})
ON CREATE SET d10.description = 'Phòng ban chức năng thực hiện công tác hành chính, tổng hợp, văn thư, lưu trữ và lễ tân tại Trường Đại học Sài Gòn.'
ON MATCH SET d10.description = 'Phòng ban chức năng thực hiện công tác hành chính, tổng hợp, văn thư, lưu trữ và lễ tân tại Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d10)
WITH u
MERGE (d11:Department {name: 'Phòng Kế hoạch - Tài chính'})
ON CREATE SET d11.description = 'Phòng ban chức năng chịu trách nhiệm lập kế hoạch, quản lý và giám sát các hoạt động tài chính, tài sản của Trường Đại học Sài Gòn.'
ON MATCH SET d11.description = 'Phòng ban chức năng chịu trách nhiệm lập kế hoạch, quản lý và giám sát các hoạt động tài chính, tài sản của Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d11)
WITH u
MERGE (d12:Department {name: 'Phòng Công tác sinh viên'})
ON CREATE SET d12.description = 'Phòng ban chức năng quản lý, hỗ trợ và thực hiện các chế độ, chính sách liên quan đến sinh viên tại Trường Đại học Sài Gòn.'
ON MATCH SET d12.description = 'Phòng ban chức năng quản lý, hỗ trợ và thực hiện các chế độ, chính sách liên quan đến sinh viên tại Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d12)
WITH u
MERGE (d13:Department {name: 'Phòng Quản lý khoa học'})
ON CREATE SET d13.description = 'Phòng ban chức năng quản lý, thúc đẩy và hỗ trợ các hoạt động nghiên cứu khoa học của cán bộ, giảng viên và sinh viên Trường Đại học Sài Gòn.'
ON MATCH SET d13.description = 'Phòng ban chức năng quản lý, thúc đẩy và hỗ trợ các hoạt động nghiên cứu khoa học của cán bộ, giảng viên và sinh viên Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d13)
WITH u
MERGE (d14:Department {name: 'Phòng Đào tạo sau đại học'})
ON CREATE SET d14.description = 'Phòng ban chức năng chịu trách nhiệm quản lý, tổ chức và giám sát công tác đào tạo trình độ thạc sĩ và tiến sĩ tại Trường Đại học Sài Gòn.'
ON MATCH SET d14.description = 'Phòng ban chức năng chịu trách nhiệm quản lý, tổ chức và giám sát công tác đào tạo trình độ thạc sĩ và tiến sĩ tại Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d14)
WITH u
MERGE (d15:Department {name: 'Phòng Thanh tra - Pháp chế'})
ON CREATE SET d15.description = 'Phòng ban chức năng thực hiện công tác thanh tra, kiểm tra việc chấp hành pháp luật và quy chế của trường; tư vấn pháp lý cho Trường Đại học Sài Gòn.'
ON MATCH SET d15.description = 'Phòng ban chức năng thực hiện công tác thanh tra, kiểm tra việc chấp hành pháp luật và quy chế của trường; tư vấn pháp lý cho Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d15)
WITH u
MERGE (d16:Department {name: 'Phòng Khảo thí & Đảm bảo chất lượng'})
ON CREATE SET d16.description = 'Phòng ban chức năng tổ chức các kỳ thi, quản lý công tác khảo thí và thực hiện các hoạt động đảm bảo chất lượng giáo dục tại Trường Đại học Sài Gòn.'
ON MATCH SET d16.description = 'Phòng ban chức năng tổ chức các kỳ thi, quản lý công tác khảo thí và thực hiện các hoạt động đảm bảo chất lượng giáo dục tại Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d16)
WITH u
MERGE (d17:Department {name: 'Ban Quản lý Dự án & Xây dựng'})
ON CREATE SET d17.description = 'Đơn vị chức năng quản lý các dự án đầu tư xây dựng cơ sở vật chất, hạ tầng của Trường Đại học Sài Gòn.'
ON MATCH SET d17.description = 'Đơn vị chức năng quản lý các dự án đầu tư xây dựng cơ sở vật chất, hạ tầng của Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d17)
WITH u
MERGE (d18:Department {name: 'Phòng Hợp tác quốc tế & Doanh nghiệp'})
ON CREATE SET d18.description = 'Phòng ban chức năng thúc đẩy và quản lý các hoạt động hợp tác quốc tế, liên kết với doanh nghiệp của Trường Đại học Sài Gòn.'
ON MATCH SET d18.description = 'Phòng ban chức năng thúc đẩy và quản lý các hoạt động hợp tác quốc tế, liên kết với doanh nghiệp của Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d18)
WITH u
MERGE (d19:Department {name: 'Phòng Thiết bị'})
ON CREATE SET d19.description = 'Phòng ban chức năng quản lý, bảo trì và cung cấp trang thiết bị phục vụ công tác giảng dạy, học tập và nghiên cứu tại Trường Đại học Sài Gòn.'
ON MATCH SET d19.description = 'Phòng ban chức năng quản lý, bảo trì và cung cấp trang thiết bị phục vụ công tác giảng dạy, học tập và nghiên cứu tại Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d19)
WITH u
MERGE (d20:Department {name: 'Phòng Giáo dục thường xuyên'})
ON CREATE SET d20.description = 'Phòng ban chức năng quản lý và tổ chức các loại hình đào tạo không chính quy như vừa làm vừa học, văn bằng hai, liên thông tại Trường Đại học Sài Gòn.'
ON MATCH SET d20.description = 'Phòng ban chức năng quản lý và tổ chức các loại hình đào tạo không chính quy như vừa làm vừa học, văn bằng hai, liên thông tại Trường Đại học Sài Gòn.'
MERGE (u)-[:hasDepartment]->(d20)
WITH u
MERGE (d21:Department {name: 'Trung tâm Khảo thí'})
ON CREATE SET d21.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, chuyên trách về công tác tổ chức thi, đánh giá năng lực và cấp chứng chỉ.'
ON MATCH SET d21.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, chuyên trách về công tác tổ chức thi, đánh giá năng lực và cấp chứng chỉ.'
MERGE (u)-[:hasDepartment]->(d21)
WITH u
MERGE (d22:Department {name: 'Trung tâm Đào tạo quốc tế'})
ON CREATE SET d22.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, triển khai các chương trình đào tạo liên kết quốc tế và dịch vụ hỗ trợ liên quan.'
ON MATCH SET d22.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, triển khai các chương trình đào tạo liên kết quốc tế và dịch vụ hỗ trợ liên quan.'
MERGE (u)-[:hasDepartment]->(d22)
WITH u
MERGE (d23:Department {name: 'Trung tâm Hỗ trợ sinh viên'})
ON CREATE SET d23.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, cung cấp các dịch vụ tư vấn, hỗ trợ việc làm, kỹ năng mềm cho sinh viên.'
ON MATCH SET d23.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, cung cấp các dịch vụ tư vấn, hỗ trợ việc làm, kỹ năng mềm cho sinh viên.'
MERGE (u)-[:hasDepartment]->(d23)
WITH u
MERGE (d24:Department {name: 'Trung tâm Học liệu'})
ON CREATE SET d24.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, quản lý thư viện, cung cấp tài nguyên thông tin, học liệu phục vụ giảng dạy và học tập.'
ON MATCH SET d24.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, quản lý thư viện, cung cấp tài nguyên thông tin, học liệu phục vụ giảng dạy và học tập.'
MERGE (u)-[:hasDepartment]->(d24)
WITH u
MERGE (d25:Department {name: 'Trung tâm Công nghệ thông tin'})
ON CREATE SET d25.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, quản lý hạ tầng mạng, hệ thống thông tin và hỗ trợ kỹ thuật công nghệ thông tin.'
ON MATCH SET d25.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, quản lý hạ tầng mạng, hệ thống thông tin và hỗ trợ kỹ thuật công nghệ thông tin.'
MERGE (u)-[:hasDepartment]->(d25)
WITH u
MERGE (d26:Department {name: 'Trung tâm Ngoại ngữ'})
ON CREATE SET d26.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, tổ chức đào tạo, bồi dưỡng và khảo thí năng lực ngoại ngữ.'
ON MATCH SET d26.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, tổ chức đào tạo, bồi dưỡng và khảo thí năng lực ngoại ngữ.'
MERGE (u)-[:hasDepartment]->(d26)
WITH u
MERGE (d27:Department {name: 'Trung tâm Tuyển sinh & Truyền thông'})
ON CREATE SET d27.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, thực hiện công tác tuyển sinh các hệ đào tạo và quản lý hoạt động truyền thông của trường.'
ON MATCH SET d27.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, thực hiện công tác tuyển sinh các hệ đào tạo và quản lý hoạt động truyền thông của trường.'
MERGE (u)-[:hasDepartment]->(d27)
WITH u
MERGE (d28:Department {name: 'Trung tâm Ký túc xá'})
ON CREATE SET d28.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, quản lý và cung cấp dịch vụ lưu trú cho sinh viên.'
ON MATCH SET d28.description = 'Trung tâm trực thuộc Trường Đại học Sài Gòn, quản lý và cung cấp dịch vụ lưu trú cho sinh viên.'
MERGE (u)-[:hasDepartment]->(d28)
WITH u
MERGE (d29:Department {name: 'Trạm Y tế'})
ON CREATE SET d29.description = 'Đơn vị trực thuộc Trường Đại học Sài Gòn, thực hiện công tác chăm sóc sức khỏe ban đầu cho cán bộ, giảng viên và sinh viên.'
ON MATCH SET d29.description = 'Đơn vị trực thuộc Trường Đại học Sài Gòn, thực hiện công tác chăm sóc sức khỏe ban đầu cho cán bộ, giảng viên và sinh viên.'
MERGE (u)-[:hasDepartment]->(d29)
WITH u
MERGE (d30:Faculty {name: 'Khoa Giáo dục Mầm non'})
ON CREATE SET d30.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo giáo viên và cán bộ quản lý trong lĩnh vực giáo dục mầm non.'
ON MATCH SET d30.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo giáo viên và cán bộ quản lý trong lĩnh vực giáo dục mầm non.'
MERGE (u)-[:hasFaculty]->(d30)
WITH u
MERGE (d31:Faculty {name: 'Khoa Giáo dục Tiểu học'})
ON CREATE SET d31.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo giáo viên và cán bộ quản lý trong lĩnh vực giáo dục tiểu học.'
ON MATCH SET d31.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo giáo viên và cán bộ quản lý trong lĩnh vực giáo dục tiểu học.'
MERGE (u)-[:hasFaculty]->(d31)
WITH u
MERGE (d32:Faculty {name: 'Khoa Sư phạm Khoa học Xã hội'})
ON CREATE SET d32.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo giáo viên các môn khoa học xã hội cho bậc phổ thông.'
ON MATCH SET d32.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo giáo viên các môn khoa học xã hội cho bậc phổ thông.'
MERGE (u)-[:hasFaculty]->(d32)
WITH u
MERGE (d33:Faculty {name: 'Khoa Sư phạm Khoa học Tự nhiên'})
ON CREATE SET d33.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo giáo viên các môn khoa học tự nhiên cho bậc phổ thông.'
ON MATCH SET d33.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo giáo viên các môn khoa học tự nhiên cho bậc phổ thông.'
MERGE (u)-[:hasFaculty]->(d33)
WITH u
MERGE (d34:Faculty {name: 'Khoa Giáo dục'})
ON CREATE SET d34.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành liên quan đến khoa học giáo dục và quản lý giáo dục.'
ON MATCH SET d34.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành liên quan đến khoa học giáo dục và quản lý giáo dục.'
MERGE (u)-[:hasFaculty]->(d34)
WITH u
MERGE (d35:Faculty {name: 'Khoa Nghệ thuật'})
ON CREATE SET d35.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành thuộc lĩnh vực nghệ thuật như mỹ thuật, âm nhạc.'
ON MATCH SET d35.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành thuộc lĩnh vực nghệ thuật như mỹ thuật, âm nhạc.'
MERGE (u)-[:hasFaculty]->(d35)
WITH u
MERGE (d36:Faculty {name: 'Khoa Ngoại ngữ'})
ON CREATE SET d36.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành ngôn ngữ và sư phạm ngoại ngữ.'
ON MATCH SET d36.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành ngôn ngữ và sư phạm ngoại ngữ.'
MERGE (u)-[:hasFaculty]->(d36)
WITH u
MERGE (d37:Faculty {name: 'Khoa Thư viện - Văn phòng'})
ON CREATE SET d37.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành liên quan đến thông tin - thư viện và quản trị văn phòng.'
ON MATCH SET d37.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành liên quan đến thông tin - thư viện và quản trị văn phòng.'
MERGE (u)-[:hasFaculty]->(d37)
WITH u
MERGE (d38:Faculty {name: 'Khoa Khoa học Môi trường'})
ON CREATE SET d38.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành thuộc lĩnh vực khoa học môi trường và quản lý tài nguyên môi trường.'
ON MATCH SET d38.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành thuộc lĩnh vực khoa học môi trường và quản lý tài nguyên môi trường.'
MERGE (u)-[:hasFaculty]->(d38)
WITH u
MERGE (d39:Faculty {name: 'Khoa Công nghệ Thông tin'})
ON CREATE SET d39.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành thuộc lĩnh vực công nghệ thông tin và khoa học máy tính.'
ON MATCH SET d39.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành thuộc lĩnh vực công nghệ thông tin và khoa học máy tính.'
MERGE (u)-[:hasFaculty]->(d39)
WITH u
MERGE (d40:Faculty {name: 'Khoa Quản trị Kinh doanh'})
ON CREATE SET d40.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành thuộc lĩnh vực quản trị kinh doanh, marketing, kinh doanh quốc tế.'
ON MATCH SET d40.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành thuộc lĩnh vực quản trị kinh doanh, marketing, kinh doanh quốc tế.'
MERGE (u)-[:hasFaculty]->(d40)
WITH u
MERGE (d41:Faculty {name: 'Khoa Tài chính - Kế toán'})
ON CREATE SET d41.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành thuộc lĩnh vực tài chính, ngân hàng, kế toán, kiểm toán.'
ON MATCH SET d41.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành thuộc lĩnh vực tài chính, ngân hàng, kế toán, kiểm toán.'
MERGE (u)-[:hasFaculty]->(d41)
WITH u
MERGE (d42:Faculty {name: 'Khoa Văn hóa và Du lịch'})
ON CREATE SET d42.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành liên quan đến văn hóa học, quản lý văn hóa và du lịch.'
ON MATCH SET d42.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành liên quan đến văn hóa học, quản lý văn hóa và du lịch.'
MERGE (u)-[:hasFaculty]->(d42)
WITH u
MERGE (d43:Faculty {name: 'Khoa Khoa học Chính trị'})
ON CREATE SET d43.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành thuộc lĩnh vực khoa học chính trị, luật.'
ON MATCH SET d43.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành thuộc lĩnh vực khoa học chính trị, luật.'
MERGE (u)-[:hasFaculty]->(d43)
WITH u
MERGE (d44:Faculty {name: 'Khoa Toán - Ứng dụng'})
ON CREATE SET d44.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành toán học, thống kê và ứng dụng toán học.'
ON MATCH SET d44.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành toán học, thống kê và ứng dụng toán học.'
MERGE (u)-[:hasFaculty]->(d44)
WITH u
MERGE (d45:Faculty {name: 'Khoa Điện tử - Viễn thông'})
ON CREATE SET d45.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành thuộc lĩnh vực kỹ thuật điện tử và viễn thông.'
ON MATCH SET d45.description = 'Khoa chuyên môn thuộc Trường Đại học Sài Gòn, đào tạo các ngành thuộc lĩnh vực kỹ thuật điện tử và viễn thông.'
MERGE (u)-[:hasFaculty]->(d45)
WITH u
MERGE (d46:Faculty {name: 'Bộ môn Giáo dục Quốc phòng & An ninh - Giáo dục Thể chất'})
ON CREATE SET d46.description = 'Đơn vị chuyên môn thuộc Trường Đại học Sài Gòn, phụ trách giảng dạy các học phần giáo dục quốc phòng, an ninh và giáo dục thể chất.'
ON MATCH SET d46.description = 'Đơn vị chuyên môn thuộc Trường Đại học Sài Gòn, phụ trách giảng dạy các học phần giáo dục quốc phòng, an ninh và giáo dục thể chất.'
MERGE (u)-[:hasFaculty]->(d46)
WITH u
MERGE (d47:Research {name: 'Viện Khoa học Dữ liệu và Trí tuệ nhân tạo'})
ON CREATE SET d47.description = 'Đơn vị nghiên cứu trực thuộc Trường Đại học Sài Gòn, tập trung vào lĩnh vực khoa học dữ liệu và trí tuệ nhân tạo.'
ON MATCH SET d47.description = 'Đơn vị nghiên cứu trực thuộc Trường Đại học Sài Gòn, tập trung vào lĩnh vực khoa học dữ liệu và trí tuệ nhân tạo.'
MERGE (u)-[:conductsResearch]->(d47)
MERGE (u)-[:hasDepartment]->(d47)
WITH u
MERGE (d48:Research {name: 'Viện Nghiên cứu Môi trường - Sức khỏe'})
ON CREATE SET d48.description = 'Đơn vị nghiên cứu trực thuộc Trường Đại học Sài Gòn, thực hiện các nghiên cứu liên quan đến môi trường và sức khỏe cộng đồng.'
ON MATCH SET d48.description = 'Đơn vị nghiên cứu trực thuộc Trường Đại học Sài Gòn, thực hiện các nghiên cứu liên quan đến môi trường và sức khỏe cộng đồng.'
MERGE (u)-[:conductsResearch]->(d48)
MERGE (u)-[:hasDepartment]->(d48)
WITH u
MERGE (d49:Department {name: 'Trung tâm Thực hành Sư phạm'})
ON CREATE SET d49.description = 'Đơn vị trực thuộc Trường Đại học Sài Gòn, tổ chức và quản lý hoạt động thực hành, thực tập sư phạm cho sinh viên.'
ON MATCH SET d49.description = 'Đơn vị trực thuộc Trường Đại học Sài Gòn, tổ chức và quản lý hoạt động thực hành, thực tập sư phạm cho sinh viên.'
MERGE (u)-[:hasDepartment]->(d49)
WITH u
MERGE (d50:Department {name: 'Trung học Thực hành Sài Gòn'})
ON CREATE SET d50.description = 'Cơ sở giáo dục phổ thông trực thuộc Trường Đại học Sài Gòn, nơi sinh viên sư phạm thực hành và thực tập giảng dạy.'
ON MATCH SET d50.description = 'Cơ sở giáo dục phổ thông trực thuộc Trường Đại học Sài Gòn, nơi sinh viên sư phạm thực hành và thực tập giảng dạy.'
MERGE (u)-[:hasDepartment]->(d50)
WITH u
MERGE (d51:Department {name: 'Tiểu học Thực hành Sài Gòn'})
ON CREATE SET d51.description = 'Cơ sở giáo dục tiểu học trực thuộc Trường Đại học Sài Gòn, nơi sinh viên sư phạm thực hành và thực tập giảng dạy.'
ON MATCH SET d51.description = 'Cơ sở giáo dục tiểu học trực thuộc Trường Đại học Sài Gòn, nơi sinh viên sư phạm thực hành và thực tập giảng dạy.'
MERGE (u)-[:hasDepartment]->(d51)