MERGE (university:University {name: 'Trường Đại học Sài Gòn', description: 'Trường Đại học Sài Gòn là cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo; là trường đại học đào tạo đa ngành, đa lĩnh vực. Trường Đại học Sài Gòn đào tạo từ trình độ đại học và sau đại học, theo 2 phương thức: chính quy và giáo dục thường xuyên (vừa làm vừa học, văn bằng hai, liên thông). Hiện nay, Trường đang tổ chức đào tạo 05 chuyên ngành tiến sĩ, 12 chuyên ngành cao học và 39 chương trình đào tạo trình độ đại học thuộc các lĩnh vực: Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm. Ngoài việc cấp bằng, Trường Đại học Sài Gòn được Bộ Giáo dục và Đào tạo cho phép đào tạo cấp các chứng chỉ Bồi dưỡng nghiệp vụ sư phạm cho giảng viên đại học, cao đẳng và bồi dưỡng nghiệp vụ sư phạm cho giáo viên Tiếng Anh Tiểu học, chứng chỉ Công nghệ Thông tin và chứng chỉ Tiếng Anh theo khung năng lực Ngoại ngữ 6 bậc dùng cho Việt Nam. Ngày 13/5/2017, Trường Đại học Sài Gòn được Chứng nhận kiểm định chất lượng giáo dục trường đại học. Năm 2018, Trường đón nhận Huân chương Lao động Hạng Ba do Chủ tịch nước Cộng hòa Xã hội Chủ nghĩa Việt Nam trao tặng.'})

MERGE (internationalCooperation:InternationalCooperation {name: 'Công tác đối ngoại', description: 'Hoạt động hợp tác quốc tế ở Trường Đại học Sài Gòn ngày càng trở nên quan trọng, duy trì và thiết lập mối quan hệ hợp tác với các trường Đại học nước ngoài và các tổ chức quốc tế ở nhiều nước trên thế giới.'})
MERGE (university)-[:hasInternationalCooperations]->(internationalCooperation)

MERGE (program1:Program {name: 'Chương trình Cử nhân Quốc tế', description: 'Chương trình Cử nhân Quốc tế Quản trị Kinh doanh và Quản lý Thương mại Điện tử được liên kết đào tạo giữa trường Đại học Sài Gòn và trường Đại học Khoa học Ứng dụng IMC Krems (Cộng hòa Áo).' })
MERGE (university)-[:offersPrograms]->(program1)

MERGE (program2:Program {name: 'Chương trình đào tạo tiếng Hoa', description: 'Chương trình đào tạo tiếng Hoa liên kết với Hiệp hội Phát triển Kinh tế Văn hóa Giáo dục Đài Việt, bao gồm Hoa ngữ giao tiếp, Luyện thi TOCFL, Hoa ngữ lớp Online.'})
MERGE (university)-[:offersPrograms]->(program2)

MERGE (scholarship1:Scholarship {name: 'Học bổng toàn phần của Bộ Y tế Singapore', description: 'Học bổng toàn phần chương trình đào tạo Trợ lý bác sĩ với trị giá SGD 120,000 từ Tập đoàn Y tế Quốc gia (MOHH), sinh viên nhận trợ cấp sinh hoạt phí và có cơ hội làm việc tại các bệnh viện hàng đầu Singapore.'})
MERGE (university)-[:awardedScholarships]->(scholarship1)

MERGE (scholarship2:Scholarship {name: 'Học bổng của Bộ Giáo dục Đài Loan', description: 'Học bổng Cử nhân hệ chính quy, vừa học vừa làm đối với các Khối ngành Kinh tế, Thương mại, Thực phẩm, Dịch vụ, Công nghệ Thông tin, Kỹ thuật, sinh viên nhận được các chính sách hỗ trợ từ Chính phủ và nhà trường.'})
MERGE (university)-[:awardedScholarships]->(scholarship2)

MERGE (program3:Program {name: 'Chương trình liên kết đào tạo', description: 'Ký kết hợp tác và xây dựng chương trình chuyển tiếp các ngành Công nghệ thông tin, Ngôn ngữ Anh, Sư phạm Anh, Quản trị kinh doanh, Tài chính - Ngân hàng thuộc Đại học Huddersfiled.'})
MERGE (university)-[:offersPrograms]->(program3)