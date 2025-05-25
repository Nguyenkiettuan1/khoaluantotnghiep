MERGE (university:University {name: 'Trường Đại học Sài Gòn', description: 'Trường Đại học Sài Gòn là cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo; là trường đại học đào tạo đa ngành, đa lĩnh vực. Trường Đại học Sài Gòn đào tạo từ trình độ đại học và sau đại học, theo 2 phương thức: chính quy và giáo dục thường xuyên (vừa làm vừa học, văn bằng hai, liên thông). Hiện nay, Trường đang tổ chức đào tạo 05 chuyên ngành tiến sĩ, 12 chuyên ngành cao học và 39 chương trình đào tạo trình độ đại học thuộc các lĩnh vực: Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm. Ngoài việc cấp bằng, Trường Đại học Sài Gòn được Bộ Giáo dục và Đào tạo cho phép đào tạo cấp các chứng chỉ Bồi dưỡng nghiệp vụ sư phạm cho giảng viên đại học, cao đẳng và bồi dưỡng nghiệp vụ sư phạm cho giáo viên Tiếng Anh Tiểu học, chứng chỉ Công nghệ Thông tin và chứng chỉ Tiếng Anh theo khung năng lực Ngoại ngữ 6 bậc dùng cho Việt Nam. Ngày 13/5/2017, Trường Đại học Sài Gòn được Chứng nhận kiểm định chất lượng giáo dục trường đại học. Năm 2018, Trường đón nhận Huân chương Lao động Hạng Ba do Chủ tịch nước Cộng hòa Xã hội Chủ nghĩa Việt Nam trao tặng.'})

MERGE (leadership:Department {name: 'Ban lãnh đạo', description: 'Ban lãnh đạo của Trường Đại học Sài Gòn bao gồm Đảng ủy, Hiệu trưởng, Các Phó Hiệu trưởng và Hội đồng trường.'})
MERGE (university)-[:hasDepartments]->(leadership)

MERGE (organization:Department {name: 'Các tổ chức đoàn thể', description: 'Các tổ chức đoàn thể tại Trường Đại học Sài Gòn bao gồm Công đoàn, Đoàn Thanh niên và Hội Sinh viên.'})
MERGE (university)-[:hasDepartments]->(organization)

MERGE (functionalDepartments:Department {name: 'Các phòng ban chức năng', description: 'Các phòng ban chức năng tại Trường Đại học Sài Gòn bao gồm Đào tạo, Tổ chức - Cán bộ, Văn phòng, Kế hoạch - Tài chính, Công tác sinh viên, Quản lý khoa học, Đào tạo sau đại học, Thanh tra - Pháp chế, Khảo thí & Đảm bảo chất lượng, Ban Quản lý Dự án & Xây dựng, Hợp tác quốc tế & Doanh nghiệp, Thiết bị, Giáo dục thường xuyên.'})
MERGE (university)-[:hasDepartments]->(functionalDepartments)

MERGE (centers:Department {name: 'Các trung tâm trực thuộc', description: 'Các trung tâm trực thuộc Trường Đại học Sài Gòn bao gồm Khảo thí, Đào tạo quốc tế, Hỗ trợ sinh viên, Học liệu, Công nghệ thông tin, Ngoại ngữ, Trung tâm Tuyển sinh & Truyền thông, Trung tâm Ký túc xá, Trạm Y tế.'})
MERGE (university)-[:hasDepartments]->(centers)

MERGE (specializedFaculties:Department {name: 'Các khoa chuyên môn', description: 'Các khoa chuyên môn tại Trường Đại học Sài Gòn bao gồm Giáo dục Mầm non, Giáo dục Tiểu học, Sư phạm Khoa học Xã hội, Sư phạm Khoa học Tự nhiên, Giáo dục, Nghệ thuật, Ngoại ngữ, Thư viện - Văn phòng, Khoa học Môi trường, Công nghệ Thông tin, Quản trị Kinh doanh, Tài chính - Kế toán, Văn hóa và Du lịch, Khoa học Chính trị, Toán - Ứng dụng, Điện tử - Viễn thông, Giáo dục Quốc phòng & An ninh - Giáo dục Thể chất.'})
MERGE (university)-[:hasDepartments]->(specializedFaculties)

MERGE (subordinateUnits:Department {name: 'Đơn vị trực thuộc', description: 'Các đơn vị trực thuộc Trường Đại học Sài Gòn bao gồm Viện Khoa học Dữ liệu và Trí tuệ nhân tạo, Viện Nghiên cứu Môi trường - Sức khỏe, Trung tâm Thực hành Sư phạm, Trung học Thực hành Sài Gòn, Tiểu học Thực hành Sài Gòn.'})
MERGE (university)-[:hasDepartments]->(subordinateUnits)