MERGE (university:Truong_Dai_hoc {name: "Trường Đại học Sài Gòn", description: "Trường Đại học Sài Gòn là cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh, chịu sự quản lý nhà nước về giáo dục của Bộ Giáo dục và Đào tạo; là trường đại học đào tạo đa ngành, đa lĩnh vực. Trường đào tạo từ trình độ đại học và sau đại học, theo 2 phương thức: chính quy và giáo dục thường xuyên (vừa làm vừa học, văn bằng hai, liên thông). Được kiểm định chất lượng giáo dục năm 2017 và nhận Huân chương Lao động Hạng Ba năm 2018"})

MERGE (degree1:Degree {name: "Tiến sĩ", description: "Trình độ đào tạo tiến sĩ với 05 chuyên ngành"})
MERGE (degree2:Degree {name: "Thạc sĩ", description: "Trình độ đào tạo thạc sĩ với 12 chuyên ngành"})
MERGE (degree3:Degree {name: "Đại học", description: "Trình độ đào tạo đại học với 39 chương trình thuộc các lĩnh vực: Kinh tế - Kỹ thuật - Công nghệ, Văn hóa xã hội, chính trị, Nghệ thuật và Sư phạm"})

MERGE (program1:Program {name: "Chính quy", description: "Phương thức đào tạo chính quy"})
MERGE (program2:Program {name: "Giáo dục thường xuyên", description: "Phương thức đào tạo thường xuyên bao gồm vừa làm vừa học, văn bằng hai, liên thông"})

MERGE (cert1:Chung_chi {name: "Bồi dưỡng nghiệp vụ sư phạm", description: "Chứng chỉ Bồi dưỡng nghiệp vụ sư phạm cho giảng viên đại học, cao đẳng"})
MERGE (cert2:Chung_chi {name: "Nghiệp vụ sư phạm Tiếng Anh Tiểu học", description: "Chứng chỉ bồi dưỡng nghiệp vụ sư phạm cho giáo viên Tiếng Anh Tiểu học"})
MERGE (cert3:Chung_chi {name: "Công nghệ Thông tin", description: "Chứng chỉ Công nghệ Thông tin"})
MERGE (cert4:Chung_chi {name: "Tiếng Anh theo khung năng lực 6 bậc", description: "Chứng chỉ Tiếng Anh theo khung năng lực Ngoại ngữ 6 bậc dùng cho Việt Nam"})

MERGE (accreditation:Kiem_dinh {name: "Kiểm định chất lượng giáo dục", description: "Được chứng nhận kiểm định chất lượng giáo dục trường đại học ngày 13/5/2017"})
MERGE (award:Giai_thuong {name: "Huân chương Lao động Hạng Ba", description: "Huân chương Lao động Hạng Ba do Chủ tịch nước Cộng hòa Xã hội Chủ nghĩa Việt Nam trao tặng năm 2018"})

MERGE (university)-[:has_degree]->(degree1)
MERGE (university)-[:has_degree]->(degree2)
MERGE (university)-[:has_degree]->(degree3)

MERGE (university)-[:offers_program]->(program1)
MERGE (university)-[:offers_program]->(program2)

MERGE (university)-[:offers_certificate]->(cert1)
MERGE (university)-[:offers_certificate]->(cert2)
MERGE (university)-[:offers_certificate]->(cert3)
MERGE (university)-[:offers_certificate]->(cert4)

MERGE (university)-[:has_accreditation]->(accreditation)
MERGE (university)-[:has_award]->(award)