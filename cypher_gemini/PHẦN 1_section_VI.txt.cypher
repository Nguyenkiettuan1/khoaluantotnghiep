cypher
MATCH (u:University {name: 'Trường Đại học Sài Gòn'})
WITH u
MERGE (j_khdhsg:Journal {name: 'Tạp chí Khoa học Đại học Sài Gòn'})
ON CREATE SET j_khdhsg.description = 'Tạp chí khoa học (Scientific Journal of Saigon University) do Trường Đại học Sài Gòn là cơ quan chủ quản. ISSN: 1859-3208. Giấy phép hoạt động số 22/GP-BTTTT (23/01/2015). Phục vụ cán bộ giảng dạy, nghiên cứu, quản lý, sinh viên. Mục đích: công bố kết quả nghiên cứu của ĐHSG, trao đổi kinh nghiệm giảng dạy/học tập, cầu nối giữa trường, cơ sở giáo dục, đào tạo và thực tiễn. Được Hội đồng Chức danh Giáo sư Nhà nước công nhận tính điểm 20 ngành khoa học. Website: http://sj.sgu.edu.vn/, Email: tcdhsg@sgu.edu.vn, Điện thoại: (028) 38 321 360.'
ON MATCH SET j_khdhsg.description = 'Tạp chí khoa học (Scientific Journal of Saigon University) do Trường Đại học Sài Gòn là cơ quan chủ quản. ISSN: 1859-3208. Giấy phép hoạt động số 22/GP-BTTTT (23/01/2015). Phục vụ cán bộ giảng dạy, nghiên cứu, quản lý, sinh viên. Mục đích: công bố kết quả nghiên cứu của ĐHSG, trao đổi kinh nghiệm giảng dạy/học tập, cầu nối giữa trường, cơ sở giáo dục, đào tạo và thực tiễn. Được Hội đồng Chức danh Giáo sư Nhà nước công nhận tính điểm 20 ngành khoa học. Website: http://sj.sgu.edu.vn/, Email: tcdhsg@sgu.edu.vn, Điện thoại: (028) 38 321 360.'
MERGE (u)-[:publishesIn]->(j_khdhsg)
WITH u, j_khdhsg
MERGE (d_bbt:Department {name: 'Ban Biên tập Tạp chí Khoa học Đại học Sài Gòn'})
ON CREATE SET d_bbt.description = 'Đơn vị chịu trách nhiệm biên tập và xuất bản Tạp chí Khoa học Đại học Sài Gòn. Trụ sở: Phòng C010, 273 An Dương Vương, Phường 3, Quận 5, TP. Hồ Chí Minh. Điện thoại: (028) 38 321 360, Email: tcdhsg@sgu.edu.vn.'
ON MATCH SET d_bbt.description = 'Đơn vị chịu trách nhiệm biên tập và xuất bản Tạp chí Khoa học Đại học Sài Gòn. Trụ sở: Phòng C010, 273 An Dương Vương, Phường 3, Quận 5, TP. Hồ Chí Minh. Điện thoại: (028) 38 321 360, Email: tcdhsg@sgu.edu.vn.'
MERGE (u)-[:hasDepartment]->(d_bbt)
WITH u, j_khdhsg
MERGE (r_guidelines:Research {name: 'Quy định và thể lệ gửi bài Tạp chí Khoa học ĐHSG'})
ON CREATE SET r_guidelines.description = 'Quy định về việc gửi và đăng bài báo khoa học trên Tạp chí Khoa học Đại học Sài Gòn. Bài viết phải là công trình mới, có giá trị, chưa công bố, viết bằng tiếng Việt hoặc Anh, tuân thủ định dạng (Word, <=12 trang, font, lề, trích dẫn IEEE/APA), cấu trúc (Tên bài, Tác giả, Tóm tắt, Từ khóa, Mở đầu, Nội dung, Kết luận, Chú thích, Tài liệu tham khảo), và quy trình phản biện. Gửi bài qua email tcdhsg@sgu.edu.vn hoặc trực tiếp.'
ON MATCH SET r_guidelines.description = 'Quy định về việc gửi và đăng bài báo khoa học trên Tạp chí Khoa học Đại học Sài Gòn. Bài viết phải là công trình mới, có giá trị, chưa công bố, viết bằng tiếng Việt hoặc Anh, tuân thủ định dạng (Word, <=12 trang, font, lề, trích dẫn IEEE/APA), cấu trúc (Tên bài, Tác giả, Tóm tắt, Từ khóa, Mở đầu, Nội dung, Kết luận, Chú thích, Tài liệu tham khảo), và quy trình phản biện. Gửi bài qua email tcdhsg@sgu.edu.vn hoặc trực tiếp.'
MERGE (u)-[:conductsResearch]->(r_guidelines)