MERGE (university:Truong_Dai_hoc {name: "Trường Đại học Sài Gòn", description: "Trường Đại học Sài Gòn là cơ sở giáo dục Đại học công lập trực thuộc UBND TP. Hồ Chí Minh"})

// Hoạt động nghiên cu khoa học sinh viên
MERGE (activity1:Hoat_dong_NCKH {name: "Đề tài NCKH cấp cơ sở", description: "Sinh viên thực hiện đề tài trong 6-9 tháng dưới sự hướng dẫn của giảng viên theo Quy chế quản lý hoạt động Khoa học và Công nghệ"})
MERGE (activity2:Hoat_dong_NCKH {name: "Bài báo khoa học", description: "Sinh viên có bài báo đăng trên tạp chí chuyên ngành trong nước, quốc tế hoặc báo cáo khoa học đăng trên k yếu hội thảo"})

// Điều kiện tham gia NCKH
MERGE (condition1:Dieu_kien {name: "Kết quả học tập", description: "Điểm trung bình từ khá trở lên trong 1 năm gần nhất (khá với sinh viên làm chủ nhiệm đề tài)"})
MERGE (condition2:Dieu_kien {name: "Không bị k luật", description: "Sinh viên không bị k luật trong thời gian học tập"})
MERGE (condition3:Dieu_kien {name: "Không có đề tài hy", description: "Không có đề tài bị hy trong năm trước"})
MERGE (condition4:Dieu_kien {name: "Không có đề tài nghiệm thu không đạt", description: "Không có đề tài nghiệm thu không đạt trong năm trước"})
MERGE (condition5:Dieu_kien {name: "Tuân thủ quy định", description: "Không vi phạm các quy định tại Điều 5 Quy chế quản lý hoạt động Khoa học và Công nghệ"})

// Quyền li NCKH
MERGE (benefit1:Quyen_loi {name: "Hỗ tr kinh phí", description: "Được h tr kinh phí cho đề tài nghiệm thu đạt trở lên"})
MERGE (benefit2:Quyen_loi {name: "Cộng điểm rèn luyện", description: "Được cộng điểm rèn luyện năm học"})
MERGE (benefit3:Quyen_loi {name: "Giấy chứng nhận", description: "Được cấp giấy chứng nhận NCKH"})
MERGE (benefit4:Quyen_loi {name: "Thưng kinh phí", description: "Được thưng kinh phí theo Quy chế cho đề tài đạt loại tốt và xuất sắc"})
MERGE (benefit5:Quyen_loi {name: "Dự thi giải thưng", description: "Được xét chọn dự thi Giải thưng Sinh viên NCKH EURÉKA và Giải thưng Sinh viên NCKH cấp Bộ"})
MERGE (benefit6:Quyen_loi {name: "u tiên học bổng", description: "Được ưu tiên xét cấp học bổng và tính điểm thi đua"})

// Giải thưng NCKH
MERGE (award1:Giai_thuong {name: "Giải thưng Sinh viên NCKH EURÉKA", description: "Giải thưng do Thành Đoàn TP.HCM t chức"})
MERGE (award2:Giai_thuong {name: "Giải thưng Sinh viên NCKH", description: "Giải thưng do Bộ GD&ĐT t chức"})
MERGE (award3:Giai_thuong {name: "Giải thưng Sinh viên NCKH cấp cơ sở", description: "Giải thưng cấp trường Đại học Sài Gòn"})

// Tạp chí và hội thảo
MERGE (journal1:Tap_chi {name: "Tạp chí chuyên ngành trong nước", description: "Các tạp chí khoa học chuyên ngành được công nhận tại Việt Nam"})
MERGE (journal2:Tap_chi {name: "Tạp chí quốc tế", description: "Các tạp chí khoa học quốc tế có uy tín"})
MERGE (conference1:Hoi_thao {name: "Hội thảo cấp quốc gia", description: "Các hội thảo khoa học cấp quốc gia"})
MERGE (conference2:Hoi_thao {name: "Hội thảo quốc tế", description: "Các hội thảo khoa học quốc tế"})

// Quản lý NCKH
MERGE (dept1:Phong_ban {name: "Phòng Quản lý Khoa học", description: "Đơn vị quản lý hoạt động NCKH của trường"})

// Tạo quan hệ
MERGE (university)-[:has_research_activity]->(activity1)
MERGE (university)-[:has_research_activity]->(activity2)

// Quan hệ điều kiện NCKH
MERGE (activity1)-[:requires_condition]->(condition1)
MERGE (activity1)-[:requires_condition]->(condition2)
MERGE (activity1)-[:requires_condition]->(condition3)
MERGE (activity1)-[:requires_condition]->(condition4)
MERGE (activity1)-[:requires_condition]->(condition5)

// Quan hệ quyền li NCKH
MERGE (activity1)-[:provides_benefit]->(benefit1)
MERGE (activity1)-[:provides_benefit]->(benefit2)
MERGE (activity1)-[:provides_benefit]->(benefit3)
MERGE (activity1)-[:provides_benefit]->(benefit4)
MERGE (activity1)-[:provides_benefit]->(benefit5)
MERGE (activity1)-[:provides_benefit]->(benefit6)

// Quan hệ giải thưng
MERGE (benefit5)-[:leads_to_award]->(award1)
MERGE (benefit5)-[:leads_to_award]->(award2)
MERGE (benefit5)-[:leads_to_award]->(award3)

// Quan hệ bài báo khoa học
MERGE (activity2)-[:can_publish_in]->(journal1)
MERGE (activity2)-[:can_publish_in]->(journal2)
MERGE (activity2)-[:can_present_at]->(conference1)
MERGE (activity2)-[:can_present_at]->(conference2)

// Quan hệ quản lý
MERGE (activity1)-[:managed_by]->(dept1)
MERGE (activity2)-[:managed_by]->(dept1)