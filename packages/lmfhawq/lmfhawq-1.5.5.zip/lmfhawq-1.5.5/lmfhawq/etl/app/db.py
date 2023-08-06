from lmf.dbv2 import db_command ,db_query ,db_write
import time 
import traceback
import os 
from lmf.bigdata import pg2csv
from datetime import datetime,timedelta
import pandas as pd 
from sqlalchemy.dialects.postgresql import TEXT,BIGINT,TIMESTAMP
import requests
import os 
import wget

#生成基础一个月的csv
def est_basecsv():
    #
    conp=["gpadmin","since2015",'192.168.4.179',"base_db","v2"]
    bgdate=datetime.strftime(datetime.now()-timedelta(days=30),'%Y-%m-%d')
    bgdate1=datetime.strftime(datetime.now()-timedelta(days=30),'%Y%m%d')
    eddate=datetime.strftime(datetime.now()+timedelta(days=365),'%Y-%m-%d')
    sql="select distinct on (html_key)* from v2.t_gg where ggstart_time>='%s' and ggstart_time<'%s'"%(bgdate,eddate)
    path="D:/webroot/bstdata/base.csv"
    pg2csv(sql,conp,path,10000,sep='\001')

#每天增量导出csv
def est_cdc_csv():
    
    html_key=db_query("select max(html_key) from cdc.t_gg",dbtype="postgresql",conp=["postgres","since2015","192.168.4.174","biaost","cdc"]).iat[0,0]
    print("html_key : %d"%html_key)
    conp=["gpadmin","since2015",'192.168.4.179',"base_db","v2"]
    bgdate=datetime.strftime(datetime.now()-timedelta(days=30),'%Y-%m-%d')
    bgdate1=datetime.strftime(datetime.now()-timedelta(days=30),'%Y%m%d')
    eddate=datetime.strftime(datetime.now()+timedelta(days=365),'%Y-%m-%d')
    sql="select distinct on(html_key) * from v2.t_gg where ggstart_time>='%s' and ggstart_time<'%s' and html_key>%d "%(bgdate,eddate,html_key)
    print(sql)
    path="D:/webroot/bstdata/cdc.csv"
    pg2csv(sql,conp,path,1000,sep='\001')



#读取一个基础csv,写入conp的数据库
def basecsv_to_db(csvpath,conp,**krg):

    para={"chunksize":1000,"tb":"t_gg"}
    para.update(krg)
    chunksize=para["chunksize"]
    tb=para["tb"]

    
    dfs=pd.read_csv(csvpath,sep='\001',chunksize=chunksize)
    datadict={"gg_key":BIGINT(),"name":TEXT(),"href":TEXT(),"ggstart_time":TIMESTAMP(0)
    ,"ggtype":TEXT(),"jytype":TEXT(),"diqu":TEXT(),"quyu":TEXT(),"info":TEXT(),"create_time":TIMESTAMP(0)
    ,"html_key":BIGINT(),"page":TEXT()
    }
    count=1

    for df in dfs:
        if count==1:
            db_write(df,tb,dbtype='postgresql',datadict=datadict,conp=conp,if_exists='replace')
            print("写入第%d个df(%d)"%(count,chunksize))
        else:
            db_write(df,tb,dbtype='postgresql',datadict=datadict,conp=conp,if_exists='append')
            print("写入第%d个df(%d)"%(count,chunksize))
        count+=1
    sql="""alter table cdc.t_gg add constraint cdc_t_gg_pk_html_key primary key(html_key)"""
    db_command(sql,dbtype="postgresql",conp=conp)

#读取增量csv
def cdccsv_to_db(csvpath,conp,**krg):
    para={"chunksize":1000,"tb":"t_gg_tmp"}
    para.update(krg)
    chunksize=para["chunksize"]
    tb=para["tb"]

    dfs=pd.read_csv(csvpath,sep='\001',chunksize=chunksize)
    datadict={"gg_key":BIGINT(),"name":TEXT(),"href":TEXT(),"ggstart_time":TIMESTAMP(0)
    ,"ggtype":TEXT(),"jytype":TEXT(),"diqu":TEXT(),"quyu":TEXT(),"info":TEXT(),"create_time":TIMESTAMP(0)
    ,"html_key":BIGINT(),"page":TEXT()
    }
    count=1

    for df in dfs:
        if count==1:
            db_write(df,tb,dbtype='postgresql',datadict=datadict,conp=conp,if_exists='replace')
            print("写入第%d个df(%d)"%(count,chunksize))
        else:
            db_write(df,tb,dbtype='postgresql',datadict=datadict,conp=conp,if_exists='append')
            print("写入第%d个df(%d)"%(count,chunksize))
        count+=1
    if count==1:
        df=pd.DataFrame(data=[],columns=datadcit.columns)
        db_write(df,tb,dbtype='postgresql',datadict=datadict,conp=conp,if_exists='replace')



def insert_t_gg(conp):

    sql="insert into cdc.t_gg select * from cdc.t_gg_tmp"
    db_command(sql,dbtype="postgresql",conp=conp)


def insert_t_gg_spec(conp):

    sql="insert into cdc.t_gg select * from cdc.t_gg_tmp as a where not exists(select 1 from cdc.t_gg as b where a.html_key=b.html_key )"
    db_command(sql,dbtype="postgresql",conp=conp)

def delete_t_gg(conp):
    bgdate=datetime.strftime(datetime.now()-timedelta(days=30),'%Y-%m-%d')
    eddate=datetime.strftime(datetime.now()-timedelta(days=29),'%Y-%m-%d')
    sql="delete from cdc.t_gg where ggstart_time>='%s' and ggstart_time<'%s' "%(bgdate,eddate)
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp)


def update_fast():
    print("一、导出增量csv")
    est_cdc_csv()

    csvpath="D:/webroot/bstdata/cdc.csv"
    print(csvpath)
    conp=["postgres","since2015",'192.168.4.174','biaost','cdc'] 
    print("二、csv写入 t_gg_tmp")
    cdccsv_to_db(csvpath,conp)
    print("三、t_gg_tmp insert into t_gg")
    insert_t_gg(conp=conp)

    print("四、删除回滚的一天")

    delete_t_gg(conp)








#外部环境下载csv 更新到t_gg 里去
def update_general(conp):
    bgdate1=datetime.strftime(datetime.now()-timedelta(days=30),'%Y%m%d')
    url_file="http://zhulong.com.cn/bstdata/cdc.csv"
    print("一、下载文件")
    if not os.path.exists("/bsttmp"):
        os.mkdir("/bsttmp")
    csvpath="/bsttmp/cdc.csv"
    r = requests.get(url_file, stream=True)
    f = open(csvpath, "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
    f.close()
    print("二、csv写入 t_gg_tmp")
    cdccsv_to_db(csvpath,conp)
    print("三、t_gg_tmp insert into t_gg")
    insert_t_gg(conp=conp)
    print("四、删除回滚的一天")

    delete_t_gg(conp)


def baseinit(conp,**krg):
    bgdate1=datetime.strftime(datetime.now()-timedelta(days=30),'%Y%m%d')
    url_file="http://www.zhulong.com.cn/bstdata/base.csv"
    print("一、下载文件")
    if not os.path.exists("/bsttmp"):
        os.mkdir("/bsttmp")
    csvpath="/bsttmp/base.csv"
    # r = requests.get(url_file, stream=True)
    # f = open(csvpath, "wb")
    # for chunk in r.iter_content(chunk_size=512):
    #     if chunk:
    #         f.write(chunk)
    # f.close()
    wget.download(url_file,'/bsttmp')
    print("二、csv写入 t_gg")
    basecsv_to_db(csvpath,conp,**krg)


def update_general_spec(conp):
    bgdate1=datetime.strftime(datetime.now()-timedelta(days=30),'%Y%m%d')
    url_file="http://zhulong.com.cn/bstdata/cdc_spec.csv"
    print("一、下载文件")
    if not os.path.exists("/bsttmp"):
        os.mkdir("/bsttmp")
    csvpath="/bsttmp/cdc.csv"
    r = requests.get(url_file, stream=True)
    f = open(csvpath, "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
    f.close()
    print("二、csv写入 t_gg_tmp")
    cdccsv_to_db(csvpath,conp)
    print("三、t_gg_tmp insert into t_gg")
    insert_t_gg_spec(conp=conp)
    print("四、删除回滚的一天")

    delete_t_gg(conp)

def est_cdc_csv_spec(sql):
    
    conp=["gpadmin","since2015",'192.168.4.179',"base_db","v2"]

    print(sql)
    path="D:/webroot/bstdata/cdc_spec.csv"
    pg2csv(sql,conp,path,1000,sep='\001')



#-----------------------------------------------数据库操作

def update_tb1(conp):
    sql1="""
    create or replace function quyu2ts(quyu text) returns text 
    as 
    $$

    txt=quyu.split('_')

    txt=' '.join(txt)
    return txt 


    $$ language plpython3u; 

    create or replace function title2ts(name text) returns text 
    as 
    $$
    import jieba 

    arr=filter(lambda x:len(x)>1, jieba.lcut(name))

    result=' '.join(arr)

    return result 

    $$ language plpython3u; 


    """

    db_command(sql1,dbtype="postgresql",conp=conp)

    print('更新gg')
    sql2="""
    insert into gg(
    gg_key, name,   href,   ggstart_time,   ggtype, jytype, diqu,   quyu    ,info,  create_time,    html_key,   update_time
    ,ts_title,ts_quyu
    )

    select 
    gg_key, name,   href,   ggstart_time,   ggtype, jytype, diqu,   quyu    ,info,  create_time,    html_key,    create_time as update_time,

    title2ts(name)::tsvector,quyu2ts(quyu)::tsvector

    from cdc.t_gg as a where not exists(select 1 from gg as b where a.html_key=b.html_key )
    """
    print('更新gghtml')
    db_command(sql2,dbtype="postgresql",conp=conp)
    sql3="""
    insert into "public"."gg_html"

    select html_key,    href,   ggstart_time,   page,   name

    from cdc.t_gg  as a

    where not exists(select 1 from gg_html as b where a.html_key=b.html_key )

    """
    db_command(sql3,dbtype="postgresql",conp=conp)

    bgdate=datetime.strftime(datetime.now()-timedelta(days=30),'%Y-%m-%d')
    eddate=datetime.strftime(datetime.now()-timedelta(days=29),'%Y-%m-%d')
    sql_a="delete from public.gg where ggstart_time<'%s' "%(eddate)
    sql_b="delete from public.gg_html where  ggstart_time<'%s' "%(eddate)
    print(sql_a)
    print(sql_b)
    db_command(sql_a,dbtype="postgresql",conp=conp)
    db_command(sql_b,dbtype="postgresql",conp=conp)


# conp=["postgres","since2015",'192.168.4.174',"biaost","public"]

# update_tb1(conp)