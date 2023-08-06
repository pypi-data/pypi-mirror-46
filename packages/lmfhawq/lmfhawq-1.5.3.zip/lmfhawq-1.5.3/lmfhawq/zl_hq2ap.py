
from lmf.dbv2 import db_command ,db_query
from lmf.bigdata import pg2pg

def get_partitions(conp):
    sql="""select partitionname from pg_partitions where schemaname='v' and tablename='gg_html' order by partitionname """

    df=db_query(sql,dbtype='postgresql',conp=conp)

    return df['partitionname'].values


def gg():
    conp1=["gpadmin",'since2015','192.168.4.179','base_db','v']

    conp2=["postgres",'since2015','10.30.30.37','biaost','public']
    arr=get_partitions(conp1)

    count=0
    for quyu in arr:

        print("gg开始写入 %s"%quyu)
        sql="""
        SELECT a.*,b.html_key  FROM v."gg" as a,v.gg_html  as b where a.href=b.href  and a.ggstart_time>='2019-04-25' 
        and a.quyu ='%s' and b.quyu='%s' """%(quyu,quyu)



        if count==0:
            pg2pg(sql,'gg_cdc',conp1,conp2,chunksize=1000,if_exists='replace')
        else:
            pg2pg(sql,'gg_cdc',conp1,conp2,chunksize=1000,if_exists='append')

        count+=1


def gg_html():
    conp1=["gpadmin",'since2015','192.168.4.179','base_db','v']

    conp2=["postgres",'since2015','10.30.30.37','biaost','public']
    arr=get_partitions(conp1)

    count=0
    for quyu in arr:

        print("gg_html开始写入 %s"%quyu)
        sql="""
        SELECT b.html_key,b.href,b.page,a.*  FROM v."gg" as a,v.gg_html  as b where a.href=b.href  and a.ggstart_time>='2019-04-27' 
        and a.quyu ='%s' and b.quyu='%s' """%(quyu,quyu)



        if count==0:
            pg2pg(sql,'gg_html_cdc',conp1,conp2,chunksize=1000,if_exists='replace')
        else:
            pg2pg(sql,'gg_html_cdc',conp1,conp2,chunksize=1000,if_exists='append')

        count+=1


def gg_html_3m():
    conp1=["gpadmin",'since2015','192.168.4.179','base_db','v']

    conp2=["postgres",'since2015','10.30.30.37','biaost','public']
    arr=get_partitions(conp1)

    count=0
    for quyu in arr:

        print("gg_html开始写入 %s"%quyu)
        sql="""
        SELECT b.html_key,b.href,b.page,a.*  FROM v."gg" as a,v.gg_html  as b where a.href=b.href  and a.ggstart_time>='2019-01-01' 
        and a.quyu ='%s' and b.quyu='%s' """%(quyu,quyu)



        if count==0:
            pg2pg(sql,'gg_html3m',conp1,conp2,chunksize=1000,if_exists='replace')
        else:
            pg2pg(sql,'gg_html3m',conp1,conp2,chunksize=1000,if_exists='append')

        count+=1
