MERGE (university:Truong_dai_hoc {name: "Trường Đại học Sài Gòn", description: "Trường Đại học Sài Gòn là cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh"})

// Các đối tác quốc tế
MERGE (partner1:Doi_tac_quoc_te {name: "Đại học Khoa học Ứng dụng IMC Krems", description: "Trường đại học tại Cộng hòa Áo, đối tác liên kết đào tạo chương trình Cử nhân Quốc tế"})
MERGE (partner2:Doi_tac_quoc_te {name: "Hiệp hội Phát triển Kinh tế Văn hóa Giáo dục Đài Việt", description: "Đối tác liên kết đào tạo tiếng Hoa (Đài Loan)"})
MERGE (partner3:Doi_tac_quoc_te {name: "Trung tâm Hoa Ngữ Sư Phạm Đài Loan", description: "Trường Đại học Quốc gia Sư Phạm Đài Loan, cấp chứng chỉ tiếng Hoa"})
MERGE (partner4:Doi_tac_quoc_te {name: "Bộ Y tế Singapore", description: "Đối tác cung cấp học bổng Asian Nursing Scholarship"})
MERGE (partner5:Doi_tac_quoc_te {name: "Bộ Giáo dục Đài Loan", description: "Đối tác cung cấp học bổng Cử nhân hệ chính quy"})
MERGE (partner6:Doi_tac_quoc_te {name: "Đại học Huddersfield", description: "Đối tác liên kết đào tạo các ngành Công nghệ thông tin, Ngôn ngữ Anh, Sư phạm Anh, Quản trị kinh doanh, Tài chính - Ngân hàng"})

// Các chương trình hợp tác
MERGE (program1:Chuong_trinh_hop_tac {name: "Cử nhân Quốc tế Quản trị Kinh doanh và Quản lý Thương mại Điện tử", description: "Chương trình liên kết với Đại học Khoa học Ứng dụng IMC Krems (Áo), được Bộ GD&ĐT phê duyệt theo QĐ 1498/QĐ-BGDĐT"})
MERGE (program2:Chuong_trinh_hop_tac {name: "Đào tạo tiếng Hoa (Đài Loan)", description: "Chương trình liên kết với Hiệp hội Đài Việt, bao gồm Hoa ngữ giao tiếp, Luyện thi TOCFL, Hoa ngữ lớp Online"})
MERGE (program3:Chuong_trinh_hop_tac {name: "Asian Nursing Scholarship", description: "Học bổng toàn phần đào tạo Trợ lý bác sĩ tại Singapore, trị giá SGD 120,000, hỗ trợ sinh hoạt phí, ký túc xá, cơ hội nhập quốc tịch"})
MERGE (program4:Chuong_trinh_hop_tac {name: "Học bổng Đài Loan", description: "Học bổng Cử nhân hệ chính quy các ngành Kinh tế, Thương mại, CNTT, Kỹ thuật với hỗ trợ học phí, ký túc xá, thực tập có lương"})
MERGE (program5:Chuong_trinh_hop_tac {name: "Liên kết đào tạo với Đại học Huddersfield", description: "Chương trình chuyển tiếp các ngành CNTT, Ngôn ngữ Anh, Sư phạm Anh, Quản trị kinh doanh, Tài chính - Ngân hàng"})
MERGE (program6:Chuong_trinh_hop_tac {name: "Thạc sĩ Giảng dạy tiếng Anh (TESOL)", description: "Chương trình liên kết với Đại học Huddersfield (Anh) đào tạo Thạc sĩ TESOL"})

// Các quốc gia hợp tác
MERGE (country1:Quoc_gia {name: "Áo", description: "Cộng hòa Áo, đối tác chương trình Cử nhân Quốc tế"})
MERGE (country2:Quoc_gia {name: "Đài Loan", description: "Đối tác đào tạo tiếng Hoa và học bổng"})
MERGE (country3:Quoc_gia {name: "Singapore", description: "Đối tác học bổng ngành y tế"})
MERGE (country4:Quoc_gia {name: "Anh", description: "Vương quốc Anh, đối tác liên kết đào tạo với Đại học Huddersfield"})

// Tạo quan hệ
MERGE (university)-[:has_international_cooperation]->(program1)
MERGE (university)-[:has_international_cooperation]->(program2)
MERGE (university)-[:has_international_cooperation]->(program3)
MERGE (university)-[:has_international_cooperation]->(program4)
MERGE (university)-[:has_international_cooperation]->(program5)
MERGE (university)-[:has_international_cooperation]->(program6)

MERGE (program1)-[:with_partner]->(partner1)
MERGE (program2)-[:with_partner]->(partner2)
MERGE (program2)-[:with_partner]->(partner3)
MERGE (program3)-[:with_partner]->(partner4)
MERGE (program4)-[:with_partner]->(partner5)
MERGE (program5)-[:with_partner]->(partner6)
MERGE (program6)-[:with_partner]->(partner6)

MERGE (partner1)-[:from_country]->(country1)
MERGE (partner2)-[:from_country]->(country2)
MERGE (partner3)-[:from_country]->(country2)
MERGE (partner4)-[:from_country]->(country3)
MERGE (partner5)-[:from_country]->(country2)
MERGE (partner6)-[:from_country]->(country4)

// Liên kết với các ngành đào tạo đã có
MATCH (major29:Nganh_dao_tao {name: "Quản trị Kinh doanh"})
MATCH (major19:Nganh_dao_tao {name: "Công nghệ Thông tin"})
MATCH (major27:Nganh_dao_tao {name: "Ngôn ngữ Anh"})
MATCH (major32:Nganh_dao_tao {name: "Tài chính - Ngân hàng"})

MERGE (program1)-[:related_to_major]->(major29)
MERGE (program5)-[:related_to_major]->(major19)
MERGE (program5)-[:related_to_major]->(major27)
MERGE (program5)-[:related_to_major]->(major29)
MERGE (program5)-[:related_to_major]->(major32)
MERGE (program6)-[:related_to_major]->(major27)