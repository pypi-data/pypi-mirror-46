from lmf.dbv2 import db_command ,db_query




#为 t_hxr表新增\删除分区
def add_partition(quyu,conp):
    user,password,ip,db,schema=conp
    sql="alter table %s.t_hxr add partition %s values('%s')"%(schema,quyu,quyu)
    db_command(sql,dbtype='postgresql',conp=conp)

def drop_partition(quyu,conp):
    user,password,ip,db,schema=conp
    sql="alter table %s.t_hxr drop partition for('%s')"%(schema,quyu)
    db_command(sql,dbtype='postgresql',conp=conp)



#更新gg gg_html表
def update_t_hxr(quyu,conp):

    user,password,ip,db,schema=conp

    sql=""" 
        select %s.add_quyu_hxr('%s')
    """%(schema,quyu)

    db_command(sql,dbtype='postgresql',conp=conp)



def add_quyu_t_hxr(quyu,conp):

    print("t_hxr表更新,目标锁定%s"%quyu)
    user,password,ip,db,schema=conp
    print("1、准备创建分区-%s"%quyu)
    sql="""
    SELECT  partitionname
    FROM pg_partitions
    WHERE tablename='t_hxr' and schemaname='%s'
    """%(schema)
    df=db_query(sql,dbtype="postgresql",conp=conp)
    if quyu in df["partitionname"].values:
        print("%s-partition已经存在"%quyu)

    else:
        print('%s-partition还不存在'%quyu)
        add_partition(quyu,conp)

    print("2、hawq中执行更新、插入语句")

    update_t_hxr(quyu,conp)

def add_quyu(quyu):
    conp=['gpadmin','since2015','192.168.4.179','base_db','mine']
    add_quyu_t_hxr(quyu,conp)


def get_partitions(conp):
    sql="""select partitionname from pg_partitions where schemaname='v' and tablename='gg_html' order by partitionname """

    df=db_query(sql,dbtype='postgresql',conp=conp)

    return df['partitionname'].values


def add_all():
    conp=['gpadmin','since2015','192.168.4.179','base_db','mine']
    arr=get_partitions(conp)

    for w in arr:
        add_quyu(w)