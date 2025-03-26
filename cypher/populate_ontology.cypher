MERGE (u:University {hasName: $hasName, hasPublication: $hasPublication, name: $name})
SET u.hasName = $hasName, u.hasPublication = $hasPublication, u.name = $name
RETURN u;
MERGE (p:Publication {hasName: $hasName, hasISSN: $hasISSN, hasLink: $hasLink, name: $name})
SET p = {hasName: $hasName, hasISSN: $hasISSN, hasLink: $hasLink, name: $name}
RETURN p;
MERGE (a:Node {name: 'Trường Đại học Sài Gòn'})
MERGE (b:Node {name: 'Tạp chí Khoa học Đại học Sài Gòn'})
MERGE (a)-[r:hasPublication]->(b)
RETURN type(r);
MERGE (u:University {hasName: $hasName, hasPublication: $hasPublication, name: $name})
SET u = {hasName: $hasName, hasPublication: $hasPublication, name: $name}
RETURN u;
MERGE (p:Publication {hasName: $hasName, hasISSN: $hasISSN, hasLink: $hasLink, name: $name})
SET p = {hasName: $hasName, hasISSN: $hasISSN, hasLink: $hasLink, name: $name}
RETURN p;
MERGE (d:Department {hasName: $hasName, name: $name})
SET d.hasName = $hasName, d.name = $name
RETURN d
Parameters: { "hasName": "Khoa Giáo dục", "name": "Khoa Giáo dục" };
MERGE (d:Department {hasName: $hasName, name: $name})
SET d.hasName = $hasName, d.name = $name
RETURN d;
MERGE (d:Department {hasName: 'Khoa Ngoại ngữ', name: 'Khoa Ngoại ngữ'});
MERGE (c:Course {hasName: $hasName, name: $name})
SET c = {hasName: $hasName, name: $name}
RETURN c;
MERGE (c:Course {hasName: $hasName, name: $name})
SET c.hasName = $hasName, c.name = $name
RETURN c
Parameters: { "hasName": "Cử nhân Kinh doanh", "name": "Cử nhân Kinh doanh" };
MERGE (c:Course {hasName: $hasName, name: $name})
SET c.hasName = $hasName, c.name = $name
RETURN c;
MERGE (s:Specialization {hasName: $hasName, name: $name})
SET s.hasName = $hasName, s.name = $name
RETURN s;
MERGE (s:Specialization {hasName: $hasName, name: $name})
SET s.hasName = $hasName, s.name = $name
RETURN s;
MERGE (s:Specialization {hasName: $hasName, name: $name})
ON CREATE SET s.hasName = $hasName, s.name = $name
RETURN s;
MERGE (e:EducationSystem {name: $name, hasMethod: $hasMethod, hasLinkage: $hasLinkage})
SET e.name = $name, e.hasMethod = $hasMethod, e.hasLinkage = $hasLinkage
RETURN e;
MERGE (a:Node {name: 'Trường Đại học Sài Gòn'})
MERGE (b:Node {name: 'Tạp chí Khoa học Đại học Sài Gòn'})
MERGE (a)-[r:hasPublication]->(b)
RETURN type(r);
MERGE (a:School {name: 'Trường Đại học Sài Gòn'})
MERGE (b:Department {name: 'Khoa Giáo dục'})
MERGE (a)-[r:hasDepartment]->(b)
RETURN type(r);
MERGE (a:School {name: 'Trường Đại học Sài Gòn'})
MERGE (b:Department {name: 'Khoa Kinh tế'})
MERGE (a)-[r:hasDepartment]->(b)
RETURN type(r);
MERGE (a:School {name: 'Trường Đại học Sài Gòn'})
MERGE (b:Department {name: 'Khoa Ngoại ngữ'})
MERGE (a)-[r:hasDepartment]->(b)
RETURN type(r);
MERGE (a:Node {name: 'Khoa Giáo dục'})
MERGE (b:Node {name: 'Cử nhân Giáo dục'})
MERGE (a)-[r:offersCourse]->(b)
RETURN type(r);
MERGE (a:Node {name: 'Khoa Kinh tế'})
MERGE (b:Node {name: 'Cử nhân Kinh doanh'})
MERGE (a)-[r:offersCourse]->(b)
RETURN type(r);
MERGE (a:Node {name: 'Khoa Ngoại ngữ'})
MERGE (b:Node {name: 'Cử nhân Ngôn ngữ Anh'})
MERGE (a)-[r:offersCourse]->(b)
RETURN type(r);
MERGE (a:Node {name: 'Cử nhân Giáo dục'})
MERGE (b:Node {name: 'Sư phạm Mầm non'})
MERGE (a)-[r:hasSpecialization]->(b)
RETURN type(r);
MERGE (a:Node {name: 'Cử nhân Giáo dục'})
MERGE (b:Node {name: 'Sư phạm Tiểu học'})
MERGE (a)-[r:hasSpecialization]->(b)
RETURN type(r);
MERGE (a:Node {name: 'Cử nhân Kinh doanh'})
MERGE (b:Node {name: 'Quản trị Kinh doanh'})
MERGE (a)-[r:hasSpecialization]->(b)
RETURN type(r);
MERGE (a:Node {name: 'Trường Đại học Sài Gòn'})
MERGE (b:Node {name: 'Giáo dục thường xuyên'})
MERGE (a)-[r:hasMethod]->(b)
RETURN type(r);