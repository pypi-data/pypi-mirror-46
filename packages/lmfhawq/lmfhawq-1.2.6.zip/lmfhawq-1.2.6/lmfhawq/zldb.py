from lmf.dbv2 import db_command ,db_query


#建原始表 gg
def est_gg(conp):
    user,password,ip,db,schema=conp
    sql="""create table %s.gg (
    gg_key   serial  ,
    name text not null ,
    href  text  not null ,
    ggstart_time timestamp not null  ,
    ggtype text  not null ,
    jytype text ,
    diqu text ,
    quyu text not null ,
    info text ,
    create_time timestamp)
    partition by list(quyu)
    (
    partition anhui_anqing values('anhui_anqing'),
    partition anhui_bengbu values('anhui_bengbu')
    )
    """%(schema)
    db_command(sql,dbtype='postgresql',conp=conp)






#建立主表 gg_html
def est_gghtml(conp):
    user,password,ip,db,schema=conp
    sql="""create table %s.gg_html(
        html_key serial    , 
        href text not null  ,
        page text not null ,
        quyu text  not null ,
        createtime timestamp )
        partition by list(quyu)
        (
        partition anhui_anqing values('anhui_anqing'),
        partition anhui_bengbu values('anhui_bengbu')
        )
    """%(schema)
    db_command(sql,dbtype='postgresql',conp=conp)


#为 gg表新增\删除分区
def add_partition_gg(quyu,conp):
    user,password,ip,db,schema=conp
    sql="alter table %s.gg add partition %s values('%s')"%(schema,quyu,quyu)
    db_command(sql,dbtype='postgresql',conp=conp)

def drop_partition_gg(quyu,conp):
    user,password,ip,db,schema=conp
    sql="alter table %s.gg drop partition for('%s')"%(schema,quyu)
    db_command(sql,dbtype='postgresql',conp=conp)


#为 gg_html 表新增\删除分区 

def add_partition_gghtml(quyu,conp):
    user,password,ip,db,schema=conp
    sql="alter table %s.gg_html add partition %s values('%s')"%(schema,quyu,quyu)
    db_command(sql,dbtype='postgresql',conp=conp)

def drop_partition_gghtml(quyu,conp):
    user,password,ip,db,schema=conp
    sql="alter table %s.gg_html drop partition for('%s')"%(schema,quyu)
    db_command(sql,dbtype='postgresql',conp=conp)

#更新gg gg_html表
def update_gg(quyu,conp):

    user,password,ip,db,schema=conp

    sql="""
        insert into %s.gg(name,href,ggstart_time,ggtype,jytype,diqu,quyu,info,create_time)
        SELECT 
        distinct on(name, href,ggstart_time)
        name,href,t_time(ggstart_time) ggstart_time,ggtype,jytype,diqu,quyu,info, create_time

         FROM src.gg    as a 
         where not exists (select 1 from %s.gg as b where 
        a.href=b.href and t_time(a.ggstart_time)=b.ggstart_time and a.name=b.name and b.quyu='%s') and quyu='%s'
        and gg_key not in(select gg_key from src.tmp_gg)
    """%(schema,schema,quyu,quyu)

    db_command(sql,dbtype='postgresql',conp=conp)





def update_gghtml(quyu,conp):

    user,password,ip,db,schema=conp

    sql="""
    insert into  %s.gg_html (href ,page ,quyu,createtime)


    select distinct on(href ) href,page,quyu , createtime 

    from src.gg_html  as a  where not exists (select 1 from %s.gg_html as b where a.href=b.href and quyu='%s') and quyu='%s'
    """%(schema,schema,quyu,quyu)

    db_command(sql,dbtype='postgresql',conp=conp)


def add_quyu_gg(quyu,conp):

    print("gg表更新,目标锁定%s"%quyu)
    user,password,ip,db,schema=conp
    print("1、准备创建分区-%s"%quyu)
    sql="""
    SELECT  partitionname
    FROM pg_partitions
    WHERE tablename='gg' and schemaname='%s'
    """%(schema)
    df=db_query(sql,dbtype="postgresql",conp=conp)
    if quyu in df["partitionname"].values:
        print("%s-partition已经存在"%quyu)

    else:
        print('%s-partition还不存在'%quyu)
        add_partition_gg(quyu,conp)

    print("2、hawq中执行更新、插入语句")

    update_gg(quyu,conp)


def add_quyu_gghtml(quyu,conp):

    print("gg_html表更新,目标锁定%s"%quyu)
    user,password,ip,db,schema=conp
    print("1、准备创建分区-%s"%quyu)
    sql="""
    SELECT  partitionname
    FROM pg_partitions
    WHERE tablename='gg_html' and schemaname='%s'
    """%(schema)
    df=db_query(sql,dbtype="postgresql",conp=conp)
    if quyu in df["partitionname"].values:
        print("%s-partition已经存在"%quyu)

    else:
        print('%s-partition还不存在'%quyu)
        add_partition_gghtml(quyu,conp)

    print("2、hawq中执行更新、插入语句")

    update_gghtml(quyu,conp)

def add_quyu_spec(quyu,conp):
    add_quyu_gg(quyu,conp)
    add_quyu_gghtml(quyu,conp)

def add_quyu(quyu):
    conp=['gpadmin','since2015','192.168.4.179','base_db','v']
    add_quyu_gg(quyu,conp)
    add_quyu_gghtml(quyu,conp)


def drop_quyu(quyu):
    conp=['gpadmin','since2015','192.168.4.179','base_db','v']
    drop_partition_gg(quyu,conp)
    drop_partition_gghtml(quyu,conp)


#conp=['gpadmin','since2015','192.168.4.179','base_db','v']



def add_quyu1(quyu):
    conp=['gpadmin','since2015!','192.168.169.57','base_db','v']
    add_quyu_gg(quyu,conp)
    add_quyu_gghtml(quyu,conp)


def drop_quyu1(quyu):
    conp=['gpadmin','since2015!','192.168.169.57','base_db','v']
    drop_partition_gg(quyu,conp)
    drop_partition_gghtml(quyu,conp)
