// 1. Tìm tất cả chương trình đào tạo của trường và số lượng
MATCH (u:University {name: 'Trường Đại học Sài Gòn'})-[:hasPrograms]->(p:TrainingProgram)
RETURN u.name as university, COUNT(p) as programCount, COLLECT(p.name) as programs

// 2. Liệt kê tất cả các cơ sở và diện tích
MATCH (u:University)-[:hasCampus]->(c:Campus)
RETURN c.name as campus, c.area as area
ORDER BY c.area DESC

// 3. Tìm các chương trình đào tạo quốc tế và thông tin chi tiết
MATCH (u:University)-[:hasPrograms]->(p:TrainingProgram)
WHERE p.name CONTAINS 'Quốc tế' OR p.description CONTAINS 'liên kết'
RETURN p.name as program, p.description as details

// 4. Hiển thị thông tin về học bổng
MATCH (u:University)-[:hasScholarshipPrograms]->(s:Scholarship)
RETURN s.name as scholarship, s.details as details

// 5. Tìm tất cả thông tin về tạp chí khoa học
MATCH (u:University)-[:hasPrograms]->(j:Journal)
RETURN j.name, j.ISSN, j.managedBy, j.usesCitationStandard, j.contactInfo

// 6. Liệt kê các chương trình sư phạm
MATCH (u:University)-[:hasPrograms]->(p:TrainingProgram)
WHERE p.name STARTS WITH 'Sư phạm'
RETURN p.name as program
ORDER BY p.name

// 7. Thống kê loại hình đào tạo của trường
MATCH (u:University {name: 'Trường Đại học Sài Gòn'})
RETURN u.hasTrainingLevels as levels, u.offersTrainingMethod as methods

// 8. Tìm các chương trình nghiên cứu khoa học và quy định
MATCH (u:University)-[:hasPrograms]->(r:ResearchTopic)
WHERE r.name CONTAINS 'NCKH' OR r.name CONTAINS 'nghiên cứu'
RETURN r.name as topic, r.details as details

// 9. Hiển thị thông tin về hợp tác quốc tế
MATCH (u:University)-[:hasInternationalCooperation]->(i:InternationalCooperation)
RETURN i.name, i.description

// 10. Tìm tất cả các trang thông tin và cổng thông tin đào tạo
MATCH (u:University)-[:hasPrograms]->(p:ResearchTopic)
WHERE p.name CONTAINS 'Trang' OR p.details CONTAINS 'Cổng thông tin'
RETURN p.name as portal, p.details as description

// 11. Tìm các chương trình đào tạo kết hợp CNTT hoặc Kỹ thuật
MATCH (u:University)-[:hasPrograms]->(p:TrainingProgram)
WHERE p.name CONTAINS 'Công nghệ' OR p.name CONTAINS 'Kỹ thuật'
RETURN p.name as program
ORDER BY p.name

// 12. Tổng diện tích các cơ sở của trường
MATCH (u:University)-[:hasCampus]->(c:Campus)
WITH c.area as area
WITH SUM(toFloat(REPLACE(area, ' m2', ''))) as total
RETURN 'Tổng diện tích: ' + toString(total) + ' m2' as totalArea

// 13. Tìm các chương trình có liên kết với nước ngoài
MATCH (u:University)-[:hasPrograms]->(p:TrainingProgram)
WHERE p.description CONTAINS 'Áo' OR p.description CONTAINS 'Anh' OR p.description CONTAINS 'Đài Loan'
RETURN p.name as program, p.description as internationalPartner

// 14. Thống kê số lượng chương trình theo từng loại
MATCH (u:University)-[:hasPrograms]->(p:TrainingProgram)
WITH CASE 
  WHEN p.name STARTS WITH 'Sư phạm' THEN 'Sư phạm'
  WHEN p.name CONTAINS 'Quốc tế' THEN 'Quốc tế'
  WHEN p.name CONTAINS 'Công nghệ' THEN 'Công nghệ'
  ELSE 'Khác'
END as programType, COUNT(p) as count
RETURN programType, count
ORDER BY count DESC

// 15. Tìm thông tin về quy định đăng bài tạp chí
MATCH (u:University)-[:hasPrograms]->(r:ResearchTopic)
WHERE r.name CONTAINS 'Quy định' OR r.name CONTAINS 'Thể lệ'
RETURN r.name as regulation, r.details as details

// 16. Liệt kê các chương trình đào tạo đặc biệt
MATCH (u:University)-[:hasPrograms]->(p:TrainingProgram)
WHERE p.name CONTAINS 'chất lượng cao' OR p.name CONTAINS 'liên kết' OR p.name CONTAINS 'văn bằng hai'
RETURN p.name as specialProgram, p.description as details

// 17. Tìm tất cả các cơ sở ở Quận 5
MATCH (u:University)-[:hasCampus]->(c:Campus)
WHERE c.name CONTAINS 'Q.5'
RETURN c.name as campus, c.area as area

// 18. Tìm các chương trình song ngành
MATCH (u:University)-[:hasPrograms]->(p:TrainingProgram)
WHERE p.name CONTAINS ' - '
RETURN p.name as dualProgram
ORDER BY p.name

// 19. Thống kê số lượng chương trình theo từng cấp độ
MATCH (u:University {name: 'Trường Đại học Sài Gòn'})
WITH SPLIT(u.hasTrainingLevels, ', ') as levels
UNWIND levels as level
RETURN level, COUNT(level) as count

// 20. Tìm tất cả thông tin về nghiên cứu và xuất bản
MATCH (u:University)-[:hasPrograms]->(r)
WHERE (r:ResearchTopic OR r:Journal)
AND (r.name CONTAINS 'nghiên cứu' OR r.name CONTAINS 'Tạp chí' OR r.details CONTAINS 'nghiên cứu')
RETURN r.name as research, r.details as details