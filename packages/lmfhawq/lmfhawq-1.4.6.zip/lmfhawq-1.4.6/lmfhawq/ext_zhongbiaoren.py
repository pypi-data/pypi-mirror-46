from lmf.dbv2 import db_command ,db_query

sql="select * from mine.t_hxr where quyu='hunan_chenzhou' and  html_key='3579571'"

df=db_query(sql,dbtype='postgresql',conp=['gpadmin','since2015','192.168.4.179','base_db','mine'])

