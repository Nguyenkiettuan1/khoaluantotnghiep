    cypher
    MATCH (u:University {name: 'Trường Đại học Sài Gòn'})
    WITH u
    MERGE (p_dt_gdct:Program {name: 'Giáo dục Chính trị'})
    ON CREATE SET p_dt_gdct.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_gdct.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_gdct)
    WITH u
    MERGE (p_dt_dl:Program {name: 'Du lịch'})
    ON CREATE SET p_dt_dl.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_dl.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_dl)
    WITH u
    MERGE (p_dt_gdmn:Program {name: 'Giáo dục Mầm non'})
    ON CREATE SET p_dt_gdmn.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ liên thông và vừa làm vừa học.'
    ON MATCH SET p_dt_gdmn.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ liên thông và vừa làm vừa học.'
    MERGE (u)-[:offersProgram]->(p_dt_gdmn)
    WITH u
    MERGE (p_dt_kt:Program {name: 'Kế toán'})
    ON CREATE SET p_dt_kt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ liên thông và văn bằng hai.'
    ON MATCH SET p_dt_kt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ liên thông và văn bằng hai.'
    MERGE (u)-[:offersProgram]->(p_dt_kt)
    WITH u
    MERGE (p_dt_gdth:Program {name: 'Giáo dục Tiểu học'})
    ON CREATE SET p_dt_gdth.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ liên thông, văn bằng hai và vừa làm vừa học.'
    ON MATCH SET p_dt_gdth.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ liên thông, văn bằng hai và vừa làm vừa học.'
    MERGE (u)-[:offersProgram]->(p_dt_gdth)
    WITH u
    MERGE (p_dt_khmt:Program {name: 'Khoa học Môi trường'})
    ON CREATE SET p_dt_khmt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_khmt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_khmt)
    WITH u
    MERGE (p_dt_span:Program {name: 'Sư phạm Âm nhạc'})
    ON CREATE SET p_dt_span.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_span.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_span)
    WITH u
    MERGE (p_dt_kdqt:Program {name: 'Kinh doanh Quốc tế'})
    ON CREATE SET p_dt_kdqt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_kdqt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_kdqt)
    WITH u
    MERGE (p_dt_spdl:Program {name: 'Sư phạm Địa lý'})
    ON CREATE SET p_dt_spdl.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_spdl.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_spdl)
    WITH u
    MERGE (p_dt_ktd:Program {name: 'Kỹ thuật Điện'})
    ON CREATE SET p_dt_ktd.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_ktd.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_ktd)
    WITH u
    MERGE (p_dt_sphh:Program {name: 'Sư phạm Hóa học'})
    ON CREATE SET p_dt_sphh.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_sphh.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_sphh)
    WITH u
    MERGE (p_dt_ktdtvt:Program {name: 'Kỹ thuật Điện tử - Viễn thông'})
    ON CREATE SET p_dt_ktdtvt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Có liên quan đến ngành CNKT Điện tử - Viễn thông.'
    ON MATCH SET p_dt_ktdtvt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Có liên quan đến ngành CNKT Điện tử - Viễn thông.'
    MERGE (u)-[:offersProgram]->(p_dt_ktdtvt)
    WITH u
    MERGE (p_dt_spkhtn:Program {name: 'Sư phạm Khoa học Tự nhiên'})
    ON CREATE SET p_dt_spkhtn.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_spkhtn.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_spkhtn)
    WITH u
    MERGE (p_dt_ktpm:Program {name: 'Kỹ thuật Phần mềm'})
    ON CREATE SET p_dt_ktpm.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_ktpm.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_ktpm)
    WITH u
    MERGE (p_dt_spls:Program {name: 'Sư phạm Lịch sử'})
    ON CREATE SET p_dt_spls.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_spls.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_spls)
    WITH u
    MERGE (p_dt_luat:Program {name: 'Luật'})
    ON CREATE SET p_dt_luat.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ văn bằng hai và vừa làm vừa học.'
    ON MATCH SET p_dt_luat.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ văn bằng hai và vừa làm vừa học.'
    MERGE (u)-[:offersProgram]->(p_dt_luat)
    WITH u
    MERGE (p_dt_splsdl:Program {name: 'Sư phạm Lịch sử - Địa lý'})
    ON CREATE SET p_dt_splsdl.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_splsdl.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_splsdl)
    WITH u
    MERGE (p_dt_nna:Program {name: 'Ngôn ngữ Anh'})
    ON CREATE SET p_dt_nna.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ văn bằng hai.'
    ON MATCH SET p_dt_nna.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ văn bằng hai.'
    MERGE (u)-[:offersProgram]->(p_dt_nna)
    WITH u
    MERGE (p_dt_spmt:Program {name: 'Sư phạm Mỹ thuật'})
    ON CREATE SET p_dt_spmt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_spmt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_spmt)
    WITH u
    MERGE (p_dt_qlgd:Program {name: 'Quản lý Giáo dục'})
    ON CREATE SET p_dt_qlgd.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ văn bằng hai và trình độ Thạc sĩ, Tiến sĩ.'
    ON MATCH SET p_dt_qlgd.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ văn bằng hai và trình độ Thạc sĩ, Tiến sĩ.'
    MERGE (u)-[:offersProgram]->(p_dt_qlgd)
    WITH u
    MERGE (p_dt_spnv:Program {name: 'Sư phạm Ngữ Văn'})
    ON CREATE SET p_dt_spnv.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_spnv.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_spnv)
    WITH u
    MERGE (p_dt_qtkd:Program {name: 'Quản trị Kinh doanh'})
    ON CREATE SET p_dt_qtkd.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ liên thông, văn bằng hai, vừa làm vừa học và trình độ Thạc sĩ, Tiến sĩ.'
    ON MATCH SET p_dt_qtkd.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ liên thông, văn bằng hai, vừa làm vừa học và trình độ Thạc sĩ, Tiến sĩ.'
    MERGE (u)-[:offersProgram]->(p_dt_qtkd)
    WITH u
    MERGE (p_dt_spsh:Program {name: 'Sư phạm Sinh học'})
    ON CREATE SET p_dt_spsh.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_spsh.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_spsh)
    WITH u
    MERGE (p_dt_qtvp:Program {name: 'Quản trị Văn phòng'})
    ON CREATE SET p_dt_qtvp.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_qtvp.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_qtvp)
    WITH u
    MERGE (p_dt_spta:Program {name: 'Sư phạm Tiếng Anh'})
    ON CREATE SET p_dt_spta.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_spta.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_spta)
    WITH u
    MERGE (p_dt_qth:Program {name: 'Quốc tế học'})
    ON CREATE SET p_dt_qth.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_qth.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_qth)
    WITH u
    MERGE (p_dt_spth:Program {name: 'Sư phạm Toán học'})
    ON CREATE SET p_dt_spth.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_spth.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_spth)
    WITH u
    MERGE (p_dt_tcnh:Program {name: 'Tài chính - Ngân hàng'})
    ON CREATE SET p_dt_tcnh.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ vừa làm vừa học và trình độ Thạc sĩ.'
    ON MATCH SET p_dt_tcnh.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo hệ vừa làm vừa học và trình độ Thạc sĩ.'
    MERGE (u)-[:offersProgram]->(p_dt_tcnh)
    WITH u
    MERGE (p_dt_spvl:Program {name: 'Sư phạm Vật lý'})
    ON CREATE SET p_dt_spvl.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_spvl.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_spvl)
    WITH u
    MERGE (p_dt_tlh:Program {name: 'Tâm lý học'})
    ON CREATE SET p_dt_tlh.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_tlh.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_tlh)
    WITH u
    MERGE (p_dt_cnktdtvt:Program {name: 'Công nghệ kỹ thuật Điện tử - Viễn thông'})
    ON CREATE SET p_dt_cnktdtvt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_cnktdtvt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_cnktdtvt)
    WITH u
    MERGE (p_dt_tn:Program {name: 'Thanh nhạc'})
    ON CREATE SET p_dt_tn.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_tn.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_tn)
    WITH u
    MERGE (p_dt_cnktddt:Program {name: 'Công nghệ kỹ thuật Điện, Điện tử'})
    ON CREATE SET p_dt_cnktddt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_cnktddt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_cnktddt)
    WITH u
    MERGE (p_dt_tttv:Program {name: 'Thông tin - Thư viện'})
    ON CREATE SET p_dt_tttv.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_tttv.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_tttv)
    WITH u
    MERGE (p_dt_cnktmt:Program {name: 'Công nghệ Kỹ thuật Môi trường'})
    ON CREATE SET p_dt_cnktmt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_cnktmt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_cnktmt)
    WITH u
    MERGE (p_dt_tud:Program {name: 'Toán Ứng dụng'})
    ON CREATE SET p_dt_tud.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_tud.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_tud)
    WITH u
    MERGE (p_dt_cntt:Program {name: 'Công nghệ Thông tin'})
    ON CREATE SET p_dt_cntt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo chương trình chất lượng cao và hệ liên thông.'
    ON MATCH SET p_dt_cntt.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn. Cũng có đào tạo chương trình chất lượng cao và hệ liên thông.'
    MERGE (u)-[:offersProgram]->(p_dt_cntt)
    WITH u
    MERGE (p_dt_vnh:Program {name: 'Việt Nam học'})
    ON CREATE SET p_dt_vnh.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_dt_vnh.description = 'Chương trình đào tạo đại học hệ chính quy, chương trình đại trà, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_dt_vnh)
    WITH u
    MERGE (p_clc_cntt:Program {name: 'Công nghệ Thông tin (Chất lượng cao)'})
    ON CREATE SET p_clc_cntt.description = 'Chương trình đào tạo đại học hệ chính quy, chất lượng cao, ngành Công nghệ Thông tin, thuộc Trường Đại học Sài Gòn.'
    ON MATCH SET p_clc_cntt.description = 'Chương trình đào tạo đại học hệ chính quy, chất lượng cao, ngành Công nghệ Thông tin, thuộc Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_clc_cntt)
    WITH u
    MERGE (p_ch_hhc:Program {name: 'Hóa hữu cơ (Cao học)'})
    ON CREATE SET p_ch_hhc.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Hóa hữu cơ tại Trường Đại học Sài Gòn. Có đào tạo trình độ Tiến sĩ.'
    ON MATCH SET p_ch_hhc.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Hóa hữu cơ tại Trường Đại học Sài Gòn. Có đào tạo trình độ Tiến sĩ.'
    MERGE (u)-[:offersProgram]->(p_ch_hhc)
    WITH u
    MERGE (p_ch_qtkd:Program {name: 'Quản trị Kinh doanh (Cao học)'})
    ON CREATE SET p_ch_qtkd.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Quản trị Kinh doanh tại Trường Đại học Sài Gòn. Có đào tạo trình độ Tiến sĩ.'
    ON MATCH SET p_ch_qtkd.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Quản trị Kinh doanh tại Trường Đại học Sài Gòn. Có đào tạo trình độ Tiến sĩ.'
    MERGE (u)-[:offersProgram]->(p_ch_qtkd)
    WITH u
    MERGE (p_ch_hltvhl:Program {name: 'Hóa lý thuyết và Hóa lý (Cao học)'})
    ON CREATE SET p_ch_hltvhl.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Hóa lý thuyết và Hóa lý tại Trường Đại học Sài Gòn.'
    ON MATCH SET p_ch_hltvhl.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Hóa lý thuyết và Hóa lý tại Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_ch_hltvhl)
    WITH u
    MERGE (p_ch_tcnh:Program {name: 'Tài chính – Ngân hàng (Cao học)'})
    ON CREATE SET p_ch_tcnh.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Tài chính – Ngân hàng tại Trường Đại học Sài Gòn.'
    ON MATCH SET p_ch_tcnh.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Tài chính – Ngân hàng tại Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_ch_tcnh)
    WITH u
    MERGE (p_ch_khmt:Program {name: 'Khoa học Máy tính (Cao học)'})
    ON CREATE SET p_ch_khmt.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Khoa học Máy tính tại Trường Đại học Sài Gòn.'
    ON MATCH SET p_ch_khmt.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Khoa học Máy tính tại Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_ch_khmt)
    WITH u
    MERGE (p_ch_tgt:Program {name: 'Toán Giải tích (Cao học)'})
    ON CREATE SET p_ch_tgt.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Toán Giải tích tại Trường Đại học Sài Gòn. Có đào tạo trình độ Tiến sĩ.'
    ON MATCH SET p_ch_tgt.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Toán Giải tích tại Trường Đại học Sài Gòn. Có đào tạo trình độ Tiến sĩ.'
    MERGE (u)-[:offersProgram]->(p_ch_tgt)
    WITH u
    MERGE (p_ch_lsvn:Program {name: 'Lịch sử Việt Nam (Cao học)'})
    ON CREATE SET p_ch_lsvn.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Lịch sử Việt Nam tại Trường Đại học Sài Gòn. Có đào tạo trình độ Tiến sĩ.'
    ON MATCH SET p_ch_lsvn.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Lịch sử Việt Nam tại Trường Đại học Sài Gòn. Có đào tạo trình độ Tiến sĩ.'
    MERGE (u)-[:offersProgram]->(p_ch_lsvn)
    WITH u
    MERGE (p_ch_vhvn:Program {name: 'Văn học Việt Nam (Cao học)'})
    ON CREATE SET p_ch_vhvn.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Văn học Việt Nam tại Trường Đại học Sài Gòn.'
    ON MATCH SET p_ch_vhvn.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Văn học Việt Nam tại Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_ch_vhvn)
    WITH u
    MERGE (p_ch_llppdhbmt:Program {name: 'Lý luận & Phương pháp dạy học bộ môn Toán (Cao học)'})
    ON CREATE SET p_ch_llppdhbmt.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Lý luận & Phương pháp dạy học bộ môn Toán tại Trường Đại học Sài Gòn.'
    ON MATCH SET p_ch_llppdhbmt.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Lý luận & Phương pháp dạy học bộ môn Toán tại Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_ch_llppdhbmt)
    WITH u
    MERGE (p_ch_ldsvttds:Program {name: 'Luật dân sự và tố tụng dân sự (Cao học)'})
    ON CREATE SET p_ch_ldsvttds.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Luật dân sự và tố tụng dân sự tại Trường Đại học Sài Gòn.'
    ON MATCH SET p_ch_ldsvttds.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Luật dân sự và tố tụng dân sự tại Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_ch_ldsvttds)
    WITH u
    MERGE (p_ch_nnh:Program {name: 'Ngôn ngữ học (Cao học)'})
    ON CREATE SET p_ch_nnh.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Ngôn ngữ học tại Trường Đại học Sài Gòn.'
    ON MATCH SET p_ch_nnh.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Ngôn ngữ học tại Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_ch_nnh)
    WITH u
    MERGE (p_ch_qlgd:Program {name: 'Quản lý Giáo dục (Cao học)'})
    ON CREATE SET p_ch_qlgd.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Quản lý Giáo dục tại Trường Đại học Sài Gòn. Có đào tạo trình độ Tiến sĩ.'
    ON MATCH SET p_ch_qlgd.description = 'Chương trình đào tạo trình độ Thạc sĩ (Cao học) chuyên ngành Quản lý Giáo dục tại Trường Đại học Sài Gòn. Có đào tạo trình độ Tiến sĩ.'
    MERGE (u)-[:offersProgram]->(p_ch_qlgd)
    WITH u
    MERGE (p_ts_hhc:Program {name: 'Hóa hữu cơ (Tiến sĩ)'})
    ON CREATE SET p_ts_hhc.description = 'Chương trình đào tạo trình độ Tiến sĩ chuyên ngành Hóa hữu cơ tại Trường Đại học Sài Gòn.'
    ON MATCH SET p_ts_hhc.description = 'Chương trình đào tạo trình độ Tiến sĩ chuyên ngành Hóa hữu cơ tại Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_ts_hhc)
    WITH u
    MERGE (p_ts_lsvn:Program {name: 'Lịch sử Việt Nam (Tiến sĩ)'})
    ON CREATE SET p_ts_lsvn.description = 'Chương trình đào tạo trình độ Tiến sĩ chuyên ngành Lịch sử Việt Nam tại Trường Đại học Sài Gòn.'
    ON MATCH SET p_ts_lsvn.description = 'Chương trình đào tạo trình độ Tiến sĩ chuyên ngành Lịch sử Việt Nam tại Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_ts_lsvn)
    WITH u
    MERGE (p_ts_qlgd:Program {name: 'Quản lý Giáo dục (Tiến sĩ)'})
    ON CREATE SET p_ts_qlgd.description = 'Chương trình đào tạo trình độ Tiến sĩ chuyên ngành Quản lý Giáo dục tại Trường Đại học Sài Gòn.'
    ON MATCH SET p_ts_qlgd.description = 'Chương trình đào tạo trình độ Tiến sĩ chuyên ngành Quản lý Giáo dục tại Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_ts_qlgd)
    WITH u
    MERGE (p_ts_tgt:Program {name: 'Toán Giải tích (Tiến sĩ)'})
    ON CREATE SET p_ts_tgt.description = 'Chương trình đào tạo trình độ Tiến sĩ chuyên ngành Toán Giải tích tại Trường Đại học Sài Gòn.'
    ON MATCH SET p_ts_tgt.description = 'Chương trình đào tạo trình độ Tiến sĩ chuyên ngành Toán Giải tích tại Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_ts_tgt)
    WITH u
    MERGE (p_ts_qtkd:Program {name: 'Quản trị Kinh doanh (Tiến sĩ)'})
    ON CREATE SET p_ts_qtkd.description = 'Chương trình đào tạo trình độ Tiến sĩ chuyên ngành Quản trị Kinh doanh tại Trường Đại học Sài Gòn.'
    ON MATCH SET p_ts_qtkd.description = 'Chương trình đào tạo trình độ Tiến sĩ chuyên ngành Quản trị Kinh doanh tại Trường Đại học Sài Gòn.'
    MERGE (u)-[:offersProgram]->(p_ts_qtkd)
    WITH u
    MERGE (p_gdtx_lt:Program {name: 'Đào tạo Đại học liên thông'})
    ON CREATE SET p_gdtx_lt.description = 'Loại hình đào tạo thuộc hệ Giáo dục thường xuyên tại Trường Đại học Sài Gòn, dành cho các ngành Công nghệ Thông tin, Kế toán, Quản trị Kinh doanh, Giáo dục Mầm non và Giáo dục Tiểu học.'
    ON MATCH SET p_gdtx_lt.description = 'Loại hình đào tạo thuộc hệ Giáo dục thường xuyên tại Trường Đại học Sài Gòn, dành cho các ngành Công nghệ Thông tin, Kế toán, Quản trị Kinh doanh, Giáo dục Mầm non và Giáo dục Tiểu học.'
    MERGE (u)-[:offersProgram]->(p_gdtx_lt)
    WITH u
    MERGE (p_gdtx_vb2:Program {name: 'Đào tạo văn bằng thứ hai'})
    ON CREATE SET p_gdtx_vb2.description = 'Loại hình đào tạo thuộc hệ Giáo dục thường xuyên tại Trường Đại học Sài Gòn, dành cho các ngành: Ngôn ngữ Anh, Kế toán, Luật, Quản trị Kinh doanh, Giáo dục Tiểu học và Quản lý Giáo dục.'
    ON MATCH SET p_gdtx_vb2.description = 'Loại hình đào tạo thuộc hệ Giáo dục thường xuyên tại Trường Đại học Sài Gòn, dành cho các ngành: Ngôn ngữ Anh, Kế toán, Luật, Quản trị Kinh doanh, Giáo dục Tiểu học và Quản lý Giáo dục.'
    MERGE (u)-[:offersProgram]->(p_gdtx_vb2)
    WITH u
    MERGE (p_gdtx_vlvh:Program {name: 'Đào tạo hệ đại học vừa làm vừa học (VLVH)'})
    ON CREATE SET p_gdtx_vlvh.description = 'Loại hình đào tạo thuộc hệ Giáo dục thường xuyên tại Trường Đại học Sài Gòn, dành cho các ngành Quản trị Kinh doanh, Tài chính - Ngân hàng, Kế toán, Luật, Giáo dục Tiểu học, Giáo dục Mầm non.'
    ON MATCH SET p_gdtx_vlvh.description = 'Loại hình đào tạo thuộc hệ Giáo dục thường xuyên tại Trường Đại học Sài Gòn, dành cho các ngành Quản trị Kinh doanh, Tài chính - Ngân hàng, Kế toán, Luật, Giáo dục Tiểu học, Giáo dục Mầm non.'
    MERGE (u)-[:offersProgram]->(p_gdtx_vlvh)
    WITH u
    MERGE (f1:Department {name: 'Cơ sở 273 An Dương Vương'})
    ON CREATE SET f1.description = 'Cơ sở đào tạo Đại học và Sau Đại học của Trường Đại học Sài Gòn tại địa chỉ 273 An Dương Vương, Quận 5, với diện tích 42.743 m2.'
    ON MATCH SET f1.description = 'Cơ sở đào tạo Đại học và Sau Đại học của Trường Đại học Sài Gòn tại địa chỉ 273 An Dương Vương, Quận 5, với diện tích 42.743 m2.'
    MERGE (u)-[:hasDepartment]->(f1)
    WITH u
    MERGE (f2:Department {name: 'Cơ sở 105 Bà Huyện Thanh Quan'})
    ON CREATE SET f2.description = 'Cơ sở đào tạo Đại học và Sau Đại học của Trường Đại học Sài Gòn tại địa chỉ 105 Bà Huyện Thanh Quan, Quận 3, với diện tích 4.823 m2.'
    ON MATCH SET f2.description = 'Cơ sở đào tạo Đại học và Sau Đại học của Trường Đại học Sài Gòn tại địa chỉ 105 Bà Huyện Thanh Quan, Quận 3, với diện tích 4.823 m2.'
    MERGE (u)-[:hasDepartment]->(f2)
    WITH u
    MERGE (f3:Department {name: 'Cơ sở 04 Tôn Đức Thắng'})
    ON CREATE SET f3.description = 'Cơ sở đào tạo Đại học và Sau Đại học của Trường Đại học Sài Gòn tại địa chỉ 04 Tôn Đức Thắng, Quận 1, với diện tích 19.655 m2.'
    ON MATCH SET f3.description = 'Cơ sở đào tạo Đại học và Sau Đại học của Trường Đại học Sài Gòn tại địa chỉ 04 Tôn Đức Thắng, Quận 1, với diện tích 19.655 m2.'
    MERGE (u)-[:hasDepartment]->(f3)
    WITH u
    MERGE (f4:Department {name: 'Ký túc xá 99 An Dương Vương'})
    ON CREATE SET f4.description = 'Ký túc xá Sinh viên của Trường Đại học Sài Gòn tại địa chỉ 99 An Dương Vương, Quận 8, với diện tích 4.800 m2.'
    ON MATCH SET f4.description = 'Ký túc xá Sinh viên của Trường Đại học Sài Gòn tại địa chỉ 99 An Dương Vương, Quận 8, với diện tích 4.800 m2.'
    MERGE (u)-[:hasDepartment]->(f4)