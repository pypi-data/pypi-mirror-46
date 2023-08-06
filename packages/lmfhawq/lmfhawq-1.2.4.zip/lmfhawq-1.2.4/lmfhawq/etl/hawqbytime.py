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
    partition by range(ggstart_time)
      (
      
    partition p2010_before start(date'1800-01-01') inclusive ,
    partition p2010 start(date'2010-01-01') inclusive ,

    partition p2011 start(date'2011-01-01') inclusive ,

    partition p2012 start(date'2012-01-01') inclusive ,

    partition p2013 start(date'2013-01-01') inclusive ,

    partition p2014 start(date'2014-01-01') inclusive ,

    partition p2015 start(date'2015-01-01') inclusive ,

    partition p2016 start(date'2016-01-01') inclusive ,

    partition p2017 start(date'2017-01-01') inclusive ,

    partition p2017b start(date'2017-07-01') inclusive ,

    partition p2018 start(date'2018-01-01') inclusive ,

    partition p2018b start(date'2018-07-01') inclusive ,

    partition p2019 start(date'2019-01-01') inclusive ,

    partition p2019b start(date'2019-07-01') inclusive 

    end (date '2020-01-01') exclusive
    )
    """%(schema)
    db_command(sql,dbtype='postgresql',conp=conp)




def export_dates_quyu(date1,date2,quyu,conp):
    sql="""
    insert into v2.t_gg 
    select a.*,html_key,page from 

    (
    select * from v.gg where quyu='%s'  and ggstart_time>='%s' and ggstart_time<'%s'

    ) a
    ,
    (select * from v.gg_html where quyu='%s')b 

    where a.href=b.href and not exists(select 1 from v2.t_gg as c where c.gg_key=a.gg_key and c.quyu='%s' and c.ggstart_time>='%s' and c.ggstart_time<'%s')

    """%(quyu,date1,date2,quyu,quyu,date1,date2)

    db_command(sql,dbtype="postgresql",conp=conp)

def export_dates(date1,date2,conp):
    sql="""
    SELECT  partitionname
    FROM pg_partitions
    WHERE tablename='gg_html' and schemaname='v' order by partitionname
    """
    df=db_query(sql,dbtype="postgresql",conp=conp)
    bg1=time.time()
    i=1
    for quyu in df['partitionname'].values[295:]:
        try:
            print("(%d) : %s"%(i,quyu))
            bg=time.time()
            export_dates_quyu(date1,date2,quyu,conp)
            ed=time.time()
            cost=int(ed-bg)
            print("耗时%d秒"%cost)
        except:

            traceback.print_exc()
        i+=1
    ed1=time.time()
    cost1=int(ed1-bg1)
    print("%s-%s----------------------------------------总耗时 %d秒--------------------------------------------------------------)"%(date1,date2,cost1))


conp=["gpadmin","since2015",'192.168.4.179',"base_db","v2"]

export_dates('2019-01-01','2019-07-01',conp=conp)

