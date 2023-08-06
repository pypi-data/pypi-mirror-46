from lmf.dbv2 import db_command ,db_query
from lmf.bigdata import pg2pg
#将 app中 gg_cdc更新到 gg表中

def gg():
    print("gg表插入")
    sql="""
    insert into gg(gg_key,html_key,name,href,ggstart_time,ggtype,jytype,diqu,quyu,info,create_time,update_time) 

    select gg_key,html_key,name,href,ggstart_time,ggtype,jytype,diqu,quyu,info,create_time , create_time as update_time

    from gg_cdc as b

    where not exists(select 1 from gg as a where a.gg_key=b.gg_key) 

    """

    db_command(sql,dbtype="postgresql",conp=["postgres",'since2015','10.30.30.37','biaost','public'])

    print("tsvector 的update")

    sql2="""
    update gg set ts_title=ext_vector(name)::tsvector where ts_title is null ;



    update gg set ts_quyu=ext_vector(quyu)::tsvector where ts_quyu is null 
    """
    db_command(sql2,dbtype="postgresql",conp=["postgres",'since2015','10.30.30.37','biaost','public'])

def gg_html():
    sql2="""

    insert into gg_html (html_key,href,ggstart_time,page,name)

    select html_key,href,ggstart_time,page,name from gg_html_cdc as a 

    where  not exists (select 1 from gg_html as b where a.html_key=b.html_key::int )
    """
    db_command(sql2,dbtype="postgresql",conp=["postgres",'since2015','10.30.30.37','biaost','public'])



#中标人从 hawq导入 到 app

def zhongbiaoren_base():
    conp1=["gpadmin",'since2015','192.168.4.179','base_db','mine']

    conp2=["postgres",'since2015','10.30.30.37','biaost','public']
    sql="""

    select * from mine.t_zhongbiaoren where ggstart_time >='2019-01-01' 
    """

    pg2pg(sql,'t_zhongbiaoren',conp1,conp2,chunksize=1000)