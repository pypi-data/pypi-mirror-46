from lmf.dbv2 import db_command ,db_query
from lmf.bigdata import pg2csv
import sys 
import os 
from fabric import Connection
from lmfhawq.remote import exe_on_remote
#建原始表 gg
def est_gg(conp):
    user,password,ip,db,schema=conp
    sql="""create table %s.gg (
    gg_key   serial  ,
    name text not null ,
    href  text  not null ,
    ggstart_time text not null  ,
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


#为新插入的表建立外部表

def est_cdc_gg(quyu,addr,conp):
    #quyu="anhui_bozhou"
    arr=quyu.split("_")
    s1,s2=arr[0],'_'.join(arr[1:])
    #addr="192.168.4.187:8111"
    #conp=['gpadmin','since2015','192.168.4.179','base_db','cdc']
    sql="""create  external table cdc.gg_%s (name text ,href  text ,ggstart_time text ,ggtype text ,jytype text , diqu text ,quyu text ,info text ) 
    location('gpfdist://%s/gg_cdc_%s.csv') format 'csv' (delimiter '\001' header quote '\002') log errors into errs segment reject limit 1000;  
    """%(quyu,addr,quyu)

    db_command(sql,dbtype="postgresql",conp=conp)

def est_cdc_gghtml(quyu,addr,conp):
    #quyu="anhui_bozhou"
    arr=quyu.split("_")
    s1,s2=arr[0],'_'.join(arr[1:])
    #addr="192.168.4.187:8111"
    #conp=['gpadmin','since2015','192.168.4.179','base_db','cdc']
    sql="""create external table cdc.gg_html_%s(href text,page text,quyu text) location('gpfdist://%s/gg_html_cdc_%s.csv') 
           format 'csv' (delimiter '\001' header quote '\002') log errors into errs segment reject limit 1000;
    """%(quyu,addr,quyu)

    db_command(sql,dbtype="postgresql",conp=conp)


#将pg数据导入到文件系统下的csv

def out_gg_all(quyu,dir,conp):
    path1=os.path.join(dir,"gg_cdc_%s.csv"%quyu)
    print(path1)
    arr=quyu.split("_")
    s1,s2=arr[0],'_'.join(arr[1:])
    sql="""select name ,href,ggstart_time,ggtype,jytype,diqu,'%s'::text quyu,info from %s.gg  """%(quyu,s2)
    #df=db_query(sql=sql,dbtype="postgresql",conp=conp)

    #df.to_csv(path1,sep='\001',quotechar='\002',index=False)
    pg2csv(sql,conp,path1,chunksize=10000,sep='\001',quotechar='\002')



def out_gg_cdc(quyu,dir,conp):
    #quyu="anhui_chizhou"
    path1=os.path.join(dir,"gg_cdc_%s.csv"%quyu)
    arr=quyu.split("_")
    s1,s2=arr[0],'_'.join(arr[1:])
    sql1="select table_name  from information_schema.tables where table_schema='%s' and table_name ~'.*gg_cdc$'"%(s2)
    df1=db_query(sql=sql1,dbtype="postgresql",conp=conp)

    sqls=["""select name,href,ggstart_time from %s.%s """%(s2,w) for w in df1['table_name']]
    sql=" union all ".join(sqls)

    sql="""with b as(%s) 
       select name ,href,ggstart_time,ggtype,jytype,diqu,'%s'::text quyu,info from %s.gg as a where  exists(select 1 from b where a.name=b.name and 
       a.href=b.href and a.ggstart_time=b.ggstart_time and b.name is not null and b.href is not null and b.ggstart_time is not null ) 
     """%(sql,quyu,s2)
    #df=db_query(sql=sql,dbtype="postgresql",conp=conp)
    #df.to_csv(path1,sep='\001',quotechar='\002',index=False)
    pg2csv(sql,conp,path1,chunksize=10000,sep='\001',quotechar='\002')


def out_gghtml_all(quyu,dir,conp):
    path1=os.path.join(dir,"gg_html_cdc_%s.csv"%quyu)
    print(path1)
    arr=quyu.split("_")
    s1,s2=arr[0],'_'.join(arr[1:])
    sql="""select href,replace(replace(page,'\r',''),'\n','') page,'%s'::text as  quyu FROM %s."gg_html" """%(quyu,s2)

    #df=db_query(sql=sql,dbtype="postgresql",conp=conp)

    #df.to_csv(path1,sep='\001',quotechar='\002',index=False)

    pg2csv(sql,conp,path1,chunksize=10000,sep='\001',quotechar='\002')


def out_gghtml_cdc(quyu,dir,conp):
    path1=os.path.join(dir,"gg_html_cdc_%s.csv"%quyu)
    print(path1)
    arr=quyu.split("_")
    s1,s2=arr[0],'_'.join(arr[1:])

    sql1="select table_name  from information_schema.tables where table_schema='%s' and table_name ~'.*gg_cdc$'"%(s2)
    df1=db_query(sql=sql1,dbtype="postgresql",conp=conp)

    sqls=["select href from %s.%s"%(s2,w) for w in df1['table_name']]
    sql_=" union all ".join(sqls)


    sql="""with b as ( %s)
    select href,replace(replace(page,'\r',''),'\n','') page,'%s'::text as  quyu FROM %s."gg_html" as a where exists(select 1 from b where a.href=b.href) """%(sql_,quyu,s2)
    print(sql)

    #df=db_query(sql=sql,dbtype="postgresql",conp=conp)

    #df.to_csv(path1,sep='\001',quotechar='\002',index=False)
    pg2csv(sql,conp,path1,chunksize=10000,sep='\001',quotechar='\002')



#更新gg gg_html表
def update_gg(quyu,conp):

    user,password,ip,db,schema=conp

    sql="""
    insert into %s.gg(name,href,ggstart_time,ggtype,jytype,diqu,quyu,info,create_time)
    SELECT 
    distinct on(name, href,ggstart_time)
    name,href,ggstart_time,ggtype,jytype,diqu,quyu,info, now() as  create_time

     FROM cdc.gg_%s a where not exists (select 1 from %s.gg as b where 
    a.href=b.href and a.ggstart_time=b.ggstart_time and a.name=b.name and quyu='%s') and name is not null and href is not null and ggstart_time is not null
    """%(schema,quyu,schema,quyu)

    db_command(sql,dbtype='postgresql',conp=conp)



def update_gghtml(quyu,conp):

    user,password,ip,db,schema=conp

    sql="""
    insert into  %s.gg_html (href ,page ,quyu,createtime)


    select distinct on(href ) href,page,quyu ,now() as createtime 

    from cdc.gg_html_%s  as a  where not exists (select 1 from %s.gg_html as b where a.href=b.href and quyu='%s')
    """%(schema,quyu,schema,quyu)

    db_command(sql,dbtype='postgresql',conp=conp)




#------------------------------------------------------------------------------------------------------------

#前提是 gg表已经建好，partition 存在或不存在,cdc 存在或不存在
def add_quyu_gg(quyu,conp,conp_src,addr,dir,tag='all'):
    print("gg表更新")
    user,password,ip,db,schema=conp
    print("1、准备创建分区")
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


    print("2、准备创建外部表")

    sql="""
    select tablename from pg_tables where schemaname='cdc'
    """
    df=db_query(sql,dbtype="postgresql",conp=conp)
    ex_tb='gg_%s'%quyu
    if ex_tb in df["tablename"].values:
        print("外部表%s已经存在"%quyu)

    else:
        print('外部表%s还不存在'%quyu)
        est_cdc_gg(quyu,addr,conp)

    print("3、准备从RDBMS导出csv")
    if tag=='all':
        out_gg_all(quyu,dir,conp_src)
    else:
        out_gg_cdc(quyu,dir,conp_src)

    print("4、hawq中执行更新、插入语句")

    update_gg(quyu,conp)

def add_quyu_gghtml(quyu,conp,conp_src,addr,dir,tag='all'):
    print("gg_html表更新")
    user,password,ip,db,schema=conp
    print("1、准备创建分区")
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


    print("2、准备创建外部表")

    sql="""
    select tablename from pg_tables where schemaname='cdc'
    """
    df=db_query(sql,dbtype="postgresql",conp=conp)
    ex_tb='gg_html_%s'%quyu
    if ex_tb in df["tablename"].values:
        print("外部表%s已经存在"%quyu)

    else:
        print('外部表%s还不存在'%quyu)
        est_cdc_gghtml(quyu,addr,conp)

    print("3、准备从RDBMS导出csv")
    if tag=='all':
        out_gghtml_all(quyu,dir,conp_src)
    else:
        out_gghtml_cdc(quyu,dir,conp_src)

    print("4、hawq中执行更新、插入语句")

    update_gghtml(quyu,conp)


def add_quyu(quyu,conp,conp_src,addr='192.168.4.187:8111',dir='/data/lmf',tag='all'):
    add_quyu_gg(quyu,conp,conp_src,addr,dir,tag)
    add_quyu_gghtml(quyu,conp,conp_src,addr,dir,tag)





def add_quyu_fast_remote(quyu,tag='all'):
    cmd="""/opt/python35/bin/python3 -c "from lmfhawq.zl import add_quyu_fast;add_quyu_fast('%s','%s')" """%(quyu,tag)
    con=['192.168.4.187','root','rootHDPHAWQDatanode5@zhulong']
    exe_on_remote(cmd,con)

#另外可以考虑使用远程调用

###主要两个接口，将PG 数据导入到 HAWQ
def drop_quyu_fast(quyu):

    conp=['gpadmin','since2015','192.168.4.179','base_db','src']
    drop_partition_gghtml(quyu,conp)

    drop_partition_gg(quyu,conp)
    
###主要两个接口，HAWQ 删除src上相应分区


def add_quyu_fast_local(quyu,tag='all'):

    arr=quyu.split("_")
    db,schema=arr[0],'_'.join(arr[1:])
    conp=['gpadmin','since2015','192.168.4.179','base_db','src']
    conp_src=['postgres','since2015','192.168.4.175',db,schema]
    add_quyu(quyu,conp=conp,conp_src=conp_src,addr='192.168.4.187:8111',dir='/data/lmf',tag=tag)

def add_quyu_fast(quyu,tag='all'):
    conp_remote=["root@192.168.4.187","rootHDPHAWQDatanode5@zhulong"]
    c=Connection(conp_remote[0],connect_kwargs={"password":conp_remote[1]})
    c.run("""/opt/python35/bin/python3 -c "from lmfhawq.zl import add_quyu_fast_local;add_quyu_fast_local('%s','%s') " """%(quyu,tag))
#--------------------------------------------------------------------------------------------------------------------------------
###主要两个接口，将PG 数据导入到 HAWQ
def drop_quyu_fast1(quyu):
    conp=['gpadmin','since2015!','192.168.169.179','base_db','src']
    drop_partition_gghtml(quyu,conp)

    drop_partition_gg(quyu,conp)
    
###主要两个接口，HAWQ 删除src上相应分区
def add_quyu_fast1_local(quyu,tag='all'):
    arr=quyu.split("_")
    db,schema=arr[0],'_'.join(arr[1:])
    conp=['gpadmin','since2015!','192.168.169.57','base_db','src']
    conp_src=['postgres','zhulong.com.cn','192.168.169.47',db,schema]
    add_quyu(quyu,conp=conp,conp_src=conp_src,addr='192.168.169.53:8111',dir='/data/lmf',tag=tag)

def add_quyu_fast1(quyu,tag='all'):
    conp_remote=["root@192.168.169.53","Aa123&*(987"]
    c=Connection(conp_remote[0],connect_kwargs={"password":conp_remote[1]})
    c.run("""/opt/python35/bin/python3 -c "from lmfhawq.zl import add_quyu_fast1_local;add_quyu_fast1_local('%s','%s') " """%(quyu,tag))
#--------------------------------------------------------------------------------------------------------------------------------
###主要两个接口，将PG 数据导入到 HAWQ
def drop_quyu_fast2(quyu):
    conp=['gpadmin','since2015!','192.168.169.179','base_db','src']
    drop_partition_gghtml(quyu,conp)

    drop_partition_gg(quyu,conp)
    
###主要两个接口，HAWQ 删除src上相应分区
def add_quyu_fast2_local(quyu,tag='all'):
    arr=quyu.split("_")
    db,schema=arr[0],'_'.join(arr[1:])
    conp=['gpadmin','since2015','192.168.4.179','base_db','src']
    conp_src=['postgres','since2015','192.168.4.182',db,schema]
    add_quyu(quyu,conp=conp,conp_src=conp_src,addr='192.168.4.187:8111',dir='/data/lmf',tag=tag)


def add_quyu_fast2(quyu,tag='all'):
    conp_remote=["root@192.168.4.187","rootHDPHAWQDatanode5@zhulong"]
    c=Connection(conp_remote[0],connect_kwargs={"password":conp_remote[1]})
    c.run("""/opt/python35/bin/python3 -c "from lmfhawq.zl import add_quyu_fast2_local;add_quyu_fast2_local('%s','%s') " """%(quyu,tag))

#--------------------------------------------------------------------------------------------------------------------------------









