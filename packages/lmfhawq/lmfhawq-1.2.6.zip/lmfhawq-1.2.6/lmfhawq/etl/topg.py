from lmf.bigdata import pg2pg 
from lmf.dbv2 import db_command,db_query
import traceback
import time

#按时间分区，单线程更新
def est_t_gg(conp):
    sql="""
    CREATE TABLE  if not exists %s."t_gg" (
    gg_key bigint ,
    name text, 
    href text ,
    ggstart_time timestamp(6),
    ggtype text ,
    jytype text ,
    diqu text ,
    quyu text ,
    info text ,
    create_time timestamp(6),
    html_key int4,
    page text
    ) partition by range(ggstart_time)
    """%(conp[4])
    db_command(sql,dbtype="postgresql",conp=conp)


#创建分区，手动创建最好
#create table if not exists  t_gg_2019_part1  partition of v.t_gg for values from('2019-01-01') to ('2019-07-01')

def est_t_gg_parts(conp):
    arr=[
    ['1900-01-01','2010-01-01'],
    ['2010-01-01','2011-01-01'],
    ['2011-01-01','2012-01-01'],
    ['2012-01-01','2013-01-01'],
    ['2013-01-01','2014-01-01'],
    ['2014-01-01','2015-01-01'],
    ['2015-01-01','2016-01-01'],
    ['2016-01-01','2017-01-01'],

    ['2017-01-01','2017-07-01'],
    ['2017-07-01','2018-01-01'],

    ['2018-01-01','2018-07-01'],
    ['2018-07-01','2019-01-01'],
    

    ['2019-01-01','2019-07-01'],
    ['2019-07-01','2020-01-01'],
    ]

    for w in arr:
        if w[0][:4]=='1900':
            name="t_gg_2010_before"
        elif w[0][:4] in ['2010','2011','2012','2013','2014','2015','2016']:
            name="t_gg_%s"%(w[0][:4])
        elif w[0][:4] in ['2017','2018','2019']:
            if w[0][5:7]=='01':
                name="t_gg_%s_part1"%(w[0][:4])
            else:
                name="t_gg_%s_part2"%(w[0][:4])
        print(name)
        sql="create table if not exists  %s.%s  partition of v.t_gg for values from('%s') to ('%s')"%(conp[4],name,w[0],w[1])
        db_command(sql,dbtype="postgresql",conp=conp)


def export_dates_quyu(date1,date2,quyu,conp1,conp2):

    sql="""
    select a.*,html_key,page from 

    (
    select * from v.gg where quyu='%s' and ggstart_time>='%s'  and ggstart_time<'%s'

    ) a
    ,
    (select * from v.gg_html where quyu='%s')b 

    where a.href=b.href 
    """%(quyu,date1,date2,quyu)
    #conp1=["gpadmin","since2015",'192.168.4.179',"base_db","v"]

    #conp2=["postgres","since2015","192.168.4.188","base","v"]

    tmptb="tmptbabc"
    pg2pg(sql,tmptb,conp1,conp2,if_exists='replace',chunksize=1000)

    sql="""insert into %s.t_gg select * from %s.%s as b 
    where not exists (select 1 from %s.t_gg as a where a.gg_key=b.gg_key )"""%(conp2[4],conp2[4],tmptb,conp2[4])

    db_command(sql,dbtype="postgresql",conp=conp2)


def export_dates(date1,date2,conp1,conp2):
    sql="select partitionname from pg_partitions where schemaname='v' and tablename='gg_html' order by partitionname"
    df=db_query(sql,dbtype="postgresql",conp=conp1)
    arr=df['partitionname'].values
    i=0
    for quyu in arr:
        print(i,quyu)
        bg=time.time()
        try:
            export_dates_quyu(date1,date2,quyu,conp1,conp2)
        except:
            traceback.print_exc()
        ed=time.time()
        cost=int(ed-bg)
        print("耗时%d秒"%cost)
        i+=1




# conp1=["gpadmin","since2015",'192.168.4.179',"base_db","v"]

# conp2=["postgres","since2015","192.168.4.188","base","v"]

# export_dates('2019-01-01','2019-07-01',conp1,conp2)


def export_dates_fast(date1,date2):

    conp1=["gpadmin","since2015",'192.168.4.179',"base_db","v"]

    conp2=["postgres","since2015","192.168.4.188","base","v"]
    #est_t_gg(conp2)
    export_dates(date1,date2,conp1,conp2)


def export_all():

    arr=[
    ['1900-01-01','2010-01-01'],
    ['2010-01-01','2011-01-01'],
    ['2011-01-01','2012-01-01'],
    ['2012-01-01','2013-01-01'],
    ['2013-01-01','2014-01-01'],
    ['2014-01-01','2015-01-01'],
    ['2015-01-01','2016-01-01'],
    ['2016-01-01','2017-01-01'],

    ['2017-01-01','2017-07-01'],
    ['2017-07-01','2018-01-01'],

    ['2018-01-01','2018-07-01'],
    ['2018-07-01','2019-01-01'],
    

    ['2019-01-01','2019-07-01'],
    ['2019-07-01','2020-01-01'],
    ]
    for w in arr:
        bg=time.time()
        print(w)
        export_dates_fast(w[0],w[1])
        ed=time.time()
        cost=int(ed-bg)
        print("----------------------------------------------------耗时%d 秒-------------------------------------"%cost)


#--------------多线程

def export_dates_quyu_mt(date1,date2,quyu,conp1,conp2):

    sql="""
    select a.*,html_key,page from 

    (
    select * from v.gg where quyu='%s' and ggstart_time>='%s'  and ggstart_time<'%s'

    ) a
    ,
    (select * from v.gg_html where quyu='%s')b 

    where a.href=b.href 
    """%(quyu,date1,date2,quyu)

    tmptb="tmp_%s"%quyu
    conp3=conp2.copy()
    conp3[4]='tmp'
    pg2pg(sql,tmptb,conp1,conp3,if_exists='replace',chunksize=1000)

    sql="""insert into %s.t_gg select * from tmp.%s as b 
    where not exists (select 1 from %s.t_gg as a where a.gg_key=b.gg_key )"""%(conp2[4],tmptb,conp2[4])

    db_command(sql,dbtype="postgresql",conp=conp2)


def export_dates_mt(date1,date2,conp1,conp2):
    sql="select partitionname from pg_partitions where schemaname='v' and tablename='gg_html' order by partitionname"
    df=db_query(sql,dbtype="postgresql",conp=conp1)
    arr=df['partitionname'].values
    bg1=time.time()
    for quyu in arr:
        print(quyu)
        bg=time.time()
        try:
            export_dates_quyu_mt(date1,date2,quyu,conp1,conp2)
        except:
            traceback.print_exc()
        ed=time.time()
        cost=int(ed-bg)
        print("耗时%d秒"%cost)
    ed1=time.time()
    cost1=int(ed1-bg1)
    print("----------------------------------------------------耗时%d 秒-------------------------------------"%cost1)


def export_dates_mt_fast(date1,date2):

    conp1=["gpadmin","since2015",'192.168.4.179',"base_db","v"]

    conp2=["postgres","since2015","192.168.4.188","base","v"]
    #est_t_gg(conp2)
    export_dates_mt(date1,date2,conp1,conp2)


export_dates_fast('2018-01-01','2018-07-01')