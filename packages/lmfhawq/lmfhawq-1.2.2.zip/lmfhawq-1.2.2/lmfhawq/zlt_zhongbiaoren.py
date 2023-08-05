from lmf.dbv2 import db_command ,db_query




#为 t_hxr表新增\删除分区
def add_partition(quyu,conp):
    user,password,ip,db,schema=conp
    sql="alter table %s.t_zhongbiaoren add partition %s values('%s')"%(schema,quyu,quyu)
    db_command(sql,dbtype='postgresql',conp=conp)

def drop_partition(quyu,conp):
    user,password,ip,db,schema=conp
    sql="alter table %s.t_zhongbiaoren drop partition for('%s')"%(schema,quyu)
    db_command(sql,dbtype='postgresql',conp=conp)


#更新gg gg_html表
def update_t_zhongbiaoren(quyu,conp):

    user,password,ip,db,schema=conp

    sql=""" 
        insert into  mine.t_zhongbiaoren(gg_key,html_key,name,href,quyu,ggstart_time,ggtype,tag,zhongbiaoren,zhongbiaojia) 
        select 

        distinct on(html_key,zhongbiaoren) *

        from (SELECT gg_key,html_key,name,href,quyu,ggstart_time,ggtype,tag,mine.ext_qiye(zhongbiaoren) as zhongbiaoren,mine.ext_zbj(zhongbiaojia) zhongbiaojia 
        FROM "mine".t_hxr 

        where mine.dyzbr(tag) and quyu='%s' ) as a 

        where  not exists(select 1 from mine.t_zhongbiaoren as b where a.html_key=b.html_key and b.quyu='%s')
        order by html_key,zhongbiaoren,zhongbiaojia;
    """%(quyu,quyu)

    db_command(sql,dbtype='postgresql',conp=conp)

def add_quyu_t_zhongbiaoren(quyu,conp):

    print("t_zhongbiaoren表更新,目标锁定%s"%quyu)
    user,password,ip,db,schema=conp
    print("1、准备创建分区-%s"%quyu)
    sql="""
    SELECT  partitionname
    FROM pg_partitions
    WHERE tablename='t_zhongbiaoren' and schemaname='%s'
    """%(schema)
    df=db_query(sql,dbtype="postgresql",conp=conp)
    if quyu in df["partitionname"].values:
        print("%s-partition已经存在"%quyu)

    else:
        print('%s-partition还不存在'%quyu)
        add_partition(quyu,conp)

    print("2、hawq中执行更新、插入语句")

    update_t_zhongbiaoren(quyu,conp)

def add_quyu(quyu):
    conp=['gpadmin','since2015','192.168.4.179','base_db','mine']
    add_quyu_t_zhongbiaoren(quyu,conp)


def get_partitions(conp):
    sql="""select partitionname from pg_partitions where schemaname='mine' and tablename='t_hxr' order by partitionname """

    df=db_query(sql,dbtype='postgresql',conp=conp)

    return df['partitionname'].values


def add_all():
    conp=['gpadmin','since2015','192.168.4.179','base_db','mine']
    arr=get_partitions(conp)

    for w in arr:
        add_quyu(w)