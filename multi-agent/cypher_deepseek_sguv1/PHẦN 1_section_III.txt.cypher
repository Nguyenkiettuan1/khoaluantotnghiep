TRUNCATE DATABASE;

MERGE (u:University {name: "Trường Đại học Sài Gòn", description: "Trường đại học công lập đa ngành, đa lĩnh vực trực thuộc UBND TP. Hồ Chí Minh"});

MERGE (org1:Organization {name: "Đảng ủy", description: "Cơ quan lãnh đạo chính trị của trường"});
MERGE (org2:Organization {name: "Hiệu trưởng", description: "Người đứng đầu nhà trường"});
MERGE (org3:Organization {name: "Phó Hiệu trưởng", description: "Các phụ tá của Hiệu trưởng"});
MERGE (org4:Organization {name: "Hội đồng trường", description: "Cơ quan quản trị cao nhất của trường"});
MERGE (u)-[:hasManagement]->(org1);
MERGE (u)-[:hasManagement]->(org2);
MERGE (u)-[:hasManagement]->(org3);
MERGE (u)-[:hasManagement]->(org4);

MERGE (org5:Organization {name: "Công đoàn", description: "Tổ chức đại diện cho người lao động"});
MERGE (org6:Organization {name: "Đoàn Thanh niên", description: "Tổ chức chính trị-xã hội của thanh niên"});
MERGE (org7:Organization {name: "Hội Sinh viên", description: "Tổ chức đại diện cho sinh viên"});
MERGE (u)-[:hasManagement]->(org5);
MERGE (u)-[:hasManagement]->(org6);
MERGE (u)-[:hasManagement]->(org7);

MERGE (dept1:Department {name: "Phòng Đào tạo", description: "Quản lý công tác đào tạo"});
MERGE (