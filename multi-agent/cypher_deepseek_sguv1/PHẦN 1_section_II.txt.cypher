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
MERGE (dept2:Department {name: "Phòng Tổ chức - Cán bộ", description: "Quản lý nhân sự"});
MERGE (dept3:Department {name: "Phòng Kế hoạch - Tài chính", description: "Quản lý tài chính và kế hoạch"});
MERGE (dept4:Department {name: "Phòng Công tác sinh viên", description: "Quản lý hoạt động sinh viên"});
MERGE (dept5:Department {name: "Phòng Quản lý khoa học", description: "Quản lý hoạt động nghiên cứu"});
MERGE (u)-[:hasDepartment]->(dept1);
MERGE (u)-[hasDepartment]->(dept2);
MERGE (u)-[:hasDepartment]->(dept3);
MERGE (u)-[:hasDepartment]->(dept4);
MERGE (u)-[:hasDepartment]->(dept5);

MERGE (center1:Department {name: "Trung tâm Đào tạo quốc tế", description: "Quản lý các chương trình quốc tế"});
MERGE (center2:Department {name: "Trung tâm Công nghệ thông tin", description: "Quản lý công nghệ thông tin"});
MERGE (center3:Department {name: "Trung tâm Ngoại ngữ", description: "Đào tạo ngoại ngữ"});
MERGE (u)-[:hasDepartment]->(center1);
MERGE (u)-[:hasDepartment]->(center2);
MERGE (u)-[:hasDepartment]->(center3);

MERGE (faculty1:Department {name: "Khoa Giáo dục Mầm non", description: "Đào tạo giáo viên mầm non"});
MERGE (faculty2:Department {name: "Khoa Giáo dục Tiểu học", description: "Đào tạo giáo viên tiểu học"});
MERGE (faculty3:Department {name: "Khoa Công nghệ Thông tin", description: "Đào tạo CNTT"});
MERGE (u)-[:hasDepartment]->(faculty1);
MERGE (u)-[:hasDepartment]->(faculty2);
MERGE (u)-[:hasDepartment]->(faculty3);

MERGE (inst1:Department {name: "Viện Khoa học Dữ liệu", description: "Nghiên cứu khoa học dữ liệu"});
MERGE (inst2:Department {name: "Viện Nghiên cứu Môi trường", description: "Nghiên cứu môi trường"});
MERGE (u)-[:hasDepartment]->(inst1);
MERGE (u)-[:hasDepartment]->(inst2);

MERGE (prog1:Program {name: "Đào tạo đại