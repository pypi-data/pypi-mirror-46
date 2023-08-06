from lmf.dbv2 import db_command ,db_query
from lmf.bigdata import pg2csv
import sys 
import time

import traceback

def est_t_gg(conp):
    user,password,ip,db,schema=conp
    sql="""create table %s.t_gg (
    gg_key   bigint  ,
    name text not null ,
    href  text  not null ,
    ggstart_time timestamp not null  ,
    ggtype text  not null ,
    jytype text ,
    diqu text ,
    quyu text not null ,
    info text ,
    create_time timestamp,
    html_key bigint,
    page text
    )
    partition by list(quyu)
    (
    partition anhui_anqing values('anhui_anqing'),
    partition anhui_bengbu values('anhui_bengbu')
    )
    """%(schema)
    db_command(sql,dbtype='postgresql',conp=conp)

#为 gg表新增\删除分区
def add_partition_t_gg(quyu,conp):
    user,password,ip,db,schema=conp
    sql="alter table %s.t_gg add partition %s values('%s')"%(schema,quyu,quyu)
    db_command(sql,dbtype='postgresql',conp=conp)

def drop_partition_t_gg(quyu,conp):
    user,password,ip,db,schema=conp
    sql="alter table %s.t_gg drop partition for('%s')"%(schema,quyu)
    db_command(sql,dbtype='postgresql',conp=conp)

def add_quyu(quyu,conp):

    print("t_gg表更新")
    user,password,ip,db,schema=conp
    print("1、准备创建分区")
    sql="""
    SELECT  partitionname
    FROM pg_partitions
    WHERE tablename='t_gg' and schemaname='%s'
    """%(schema)
    df=db_query(sql,dbtype="postgresql",conp=conp)
    if quyu in df["partitionname"].values:
        print("%s-partition已经存在"%quyu)

    else:
        print('%s-partition还不存在'%quyu)
        add_partition_t_gg(quyu,conp)

    print("2、更新插入分区 %s"%quyu)
    sql="""
    insert into %s.t_gg 
    select a.*,html_key,page from 

    (
    select * from v.gg where quyu='%s' 

    ) a
    ,
    (select * from v.gg_html where quyu='%s')b 

    where a.href=b.href and not exists(select 1 from %s.t_gg as c where c.gg_key=a.gg_key and c.quyu='%s')

    """%(conp[4],quyu,quyu,conp[4],quyu)
    db_command(sql,dbtype='postgresql',conp=conp)



def add_quyu_all(conp):
    sql="""
    SELECT  partitionname
    FROM pg_partitions
    WHERE tablename='gg_html' and schemaname='v' order by partitionname
    """
    df=db_query(sql,dbtype="postgresql",conp=conp)
    bg1=time.time()
    i=1
    for quyu in df['partitionname'].values:

        print("(%d) : %s"%(i,quyu))
        
        bg=time.time()
        try:
            add_quyu(quyu,conp)
        except:
            traceback.print_exc()
        ed=time.time()
        cost=int(ed-bg)
        print("%s耗时 %d秒"%(quyu,cost))
        i+=1
    ed1=time.time()
    cost1=int(ed1-bg1)
    print("总共%d耗时"%(cost1))
    

conp=["gpadmin","since2015",'192.168.4.179',"base_db","v1"]

add_quyu_all(conp)