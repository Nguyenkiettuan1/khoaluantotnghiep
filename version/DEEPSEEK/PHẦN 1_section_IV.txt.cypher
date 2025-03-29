MERGE (university:Truong_Dai_hoc {name: "Trường Đại học Sài Gòn", description: "Trường Đại học Sài Gòn là cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh"})

// Các quốc gia hợp tác
MERGE (country1:Quoc_gia {name: "Hoa K", description: "Hp tác với các trường đại học và t chức tại Hoa K"})
MERGE (country2:Quoc_gia {name: "Anh", description: "Hp tác với các trường đại học và t chức tại Vương quốc Anh"})
MERGE (country3:Quoc_gia {name: "Nga", description: "Hp tác với các trường đại học và t chức tại Nga"})
MERGE (country4:Quoc_gia {name: "Pháp", description: "Hp tác với các trường đại học và t chức tại Pháp"})
MERGE (country5:Quoc_gia {name: "Australia", description: "Hp tác với các trường đại học và t chức tại Australia"})
MERGE (country6:Quoc_gia {name: "Trung Quốc", description: "Hp tác với các trường đại học và t chức tại Trung Quốc"})
MERGE (country7:Quoc_gia {name: "Singapore", description: "Hp tác với các trường đại học và t chức tại Singapore"})
MERGE (country8:Quoc_gia {name: "Malaysia", description: "Hp tác với các trường đại học và t chức tại Malaysia"})
MERGE (country9:Quoc_gia {name: "Cộng hòa Áo", description: "Hp tác với các trường đại học và t chức tại Cộng hòa Áo"})
MERGE (country10:Quoc_gia {name: "New Zealand", description: "Hp tác với các trường đại học và t chức tại New Zealand"})
MERGE (country11:Quoc_gia {name: "Thụy Điển", description: "Hp tác với các trường đại học và t chức tại Thụy Điển"})
MERGE (country12:Quoc_gia {name: "Đài Loan", description: "Hp tác với các trường đại học và t chức tại Đài Loan"})

// Các chương trình hợp tác quốc tế
MERGE (program1:Chuong_trinh_hop_tac {name: "Cử nhân Quốc tế Quản trị Kinh doanh và Quản lý Thương mại Điện tử", description: "Chương trình liên kết với Đại học Khoa học ng dụng IMC Krems (Áo), được Bộ GD&ĐT phê duyệt theo QĐ số 1498/QĐ-BGDĐT ngày 28/4/2014"})
MERGE (program2:Chuong_trinh_hop_tac {name: "Đào tạo tiếng Hoa (Đài Loan)", description: "Liên kết với Hiệp hội Phát triển Kinh tế Văn hóa Giáo dục Đài Việt, cấp chứng chỉ bởi Trung tâm Hoa Ngữ Sư Phạm Đài Loan"})
MERGE (program3:Chuong_trinh_hop_tac {name: "Học bổng Asian Nursing Scholarship", description: "Học bổng toàn phần ngành Tr lý bác sĩ tại Singapore trị giá SGD 120,000, h tr sinh hoạt phí, ký túc xá và cơ hội định cư"})
MERGE (program4:Chuong_trinh_hop_tac {name: "Học bổng Đài Loan", description: "Học bổng Cử nhân các ngành Kinh tế, Thương mại, CNTT, K thuật với h tr học phí, thực tập có lương"})
MERGE (program5:Chuong_trinh_hop_tac {name: "Chương trình chuyển tiếp Đại học Huddersfield", description: "Liên kết đào tạo các ngành CNTT, Ngôn ngữ Anh, Quản trị kinh doanh, Tài chính - Ngân hàng với ĐH Huddersfield (Anh)"})
MERGE (program6:Chuong_trinh_hop_tac {name: "Thạc sĩ TESOL", description: "Kế hoạch liên kết chương trình Thạc sĩ Giảng dạy tiếng Anh với ĐH Huddersfield (Anh)"})

// Các đối tác quốc tế
MERGE (partner1:Doi_tac {name: "Đại học Khoa học ng dụng IMC Krems", description: "Trường đại học tại Cộng hòa Áo, đối tác chương trình Cử nhân Quốc tế"})
MERGE (partner2:Doi_tac {name: "Hiệp hội Phát triển Kinh tế Văn hóa Giáo dục Đài Việt", description: "Đối tác chương trình đào tạo tiếng Hoa"})
MERGE (partner3:Doi_tac {name: "Bộ Y tế Singapore", description: "Đối tác chương trình học bổng Asian Nursing Scholarship"})
MERGE (partner4:Doi_tac {name: "Tập đoàn Y tế Quốc gia Singapore (MOHH)", description: "Nhà tài tr chính học bổng ngành Tr lý bác sĩ"})
MERGE (partner5:Doi_tac {name: "Bộ Giáo dục Đài Loan", description: "Đối tác chương trình học bổng Đài Loan"})
MERGE (partner6:Doi_tac {name: "Đại học Huddersfield", description: "Đối tác chương trình chuyển tiếp và Thạc sĩ TESOL tại Vương quốc Anh"})
MERGE (partner7:Doi_tac {name: "Trung tâm Hoa Ngữ Sư Phạm Đài Loan", description: "Đơn vị cấp chứng chỉ tiếng Hoa"})
MERGE (partner8:Doi_tac {name: "Đại học Quốc gia Sư Phạm Đài Loan", description: "Đơn vị đào tạo chương trình tiếng Hoa"})

// Các bệnh viện Singapore
MERGE (hospital1:Benh_vien {name: "Bệnh viện Tan Tock Seng", description: "Bệnh viện hàng đầu Singapore, nơi làm việc sau tốt nghiệp chương trình Asian Nursing Scholarship"})
MERGE (hospital2:Benh_vien {name: "Bệnh viện John Hopkins", description: "Bệnh viện quốc tế tại Singapore, nơi làm việc sau tốt nghiệp chương trình Asian Nursing Scholarship"})

// Tạo quan hệ hợp tác quốc tế
MERGE (university)-[:cooperates_with]->(country1)
MERGE (university)-[:cooperates_with]->(country2)
MERGE (university)-[:cooperates_with]->(country3)
MERGE (university)-[:cooperates_with]->(country4)
MERGE (university)-[:cooperates_with]->(country5)
MERGE (university)-[:cooperates_with]->(country6)
MERGE (university)-[:cooperates_with]->(country7)
MERGE (university)-[:cooperates_with]->(country8)
MERGE (university)-[:cooperates_with]->(country9)
MERGE (university)-[:cooperates_with]->(country10)
MERGE (university)-[:cooperates_with]->(country11)
MERGE (university)-[:cooperates_with]->(country12)

// Quan hệ chương trình hợp tác
MERGE (university)-[:has_international_program]->(program1)
MERGE (university)-[:has_international_program]->(program2)
MERGE (university)-[:has_international_program]->(program3)
MERGE (university)-[:has_international_program]->(program4)
MERGE (university)-[:has_international_program]->(program5)
MERGE (university)-[:has_international_program]->(program6)

// Quan hệ đối tác chương trình
MERGE (program1)-[:with_partner]->(partner1)
MERGE (program2)-[:with_partner]->(partner2)
MERGE (program2)-[:with_partner]->(partner7)
MERGE (program2)-[:with_partner]->(partner8)
MERGE (program3)-[:with_partner]->(partner3)
MERGE (program3)-[:with_partner]->(partner4)
MERGE (program4)-[:with_partner]->(partner5)
MERGE (program5)-[:with_partner]->(partner6)
MERGE (program6)-[:with_partner]->(partner6)

// Quan hệ bệnh viện Singapore
MERGE (program3)-[:provides_employment]->(hospital1)
MERGE (program3)-[:provides_employment]->(hospital2)

// Quan hệ quốc gia đối tác
MERGE (partner1)-[:from_country]->(country9)
MERGE (partner2)-[:from_country]->(country12)
MERGE (partner3)-[:from_country]->(country7)
MERGE (partner4)-[:from_country]->(country7)
MERGE (partner5)-[:from_country]->(country12)
MERGE (partner6)-[:from_country]->(country2)
MERGE (partner7)-[:from_country]->(country12)
MERGE (partner8)-[:from_country]->(country12)