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


#生成基础一个月的csv
def base_to_csv():
    #
    conp=["gpadmin","since2015",'192.168.4.179',"base_db","v2"]
    bgdate=datetime.strftime(datetime.now()-timedelta(days=30),'%Y-%m-%d')
    bgdate1=datetime.strftime(datetime.now()-timedelta(days=30),'%Y%m%d')
    eddate=datetime.strftime(datetime.now()+timedelta(days=365),'%Y-%m-%d')
    sql="select * from v2.t_gg where ggstart_time>='%s' and ggstart_time<'%s'"%(bgdate,eddate)
    path="D:/webroot/bstdata/base_%s.csv"%bgdate1
    pg2csv(sql,conp,path,10000,sep='\001')


#def write_all(csvpath,conp):
#基础csv入库
def csv_to_db(csvpath,conp,**krg):
    #csvpath="d:/beifen/test1.csv"
    #conp=["postgres","since2015",'192.168.4.174','biaost','cdc'] 
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

    conp=["gpadmin","since2015",'192.168.4.179',"base_db","v2"]
    bgdate=datetime.strftime(datetime.now()-timedelta(days=30),'%Y-%m-%d')
    bgdate1=datetime.strftime(datetime.now()-timedelta(days=30),'%Y%m%d')
    eddate=datetime.strftime(datetime.now()+timedelta(days=365),'%Y-%m-%d')
    sql="select * from v2.t_gg where ggstart_time>='%s' and ggstart_time<'%s'"%(bgdate,eddate)
    path="D:/webroot/bstdata/base_%s.csv"%bgdate1
    pg2csv(sql,conp,path,10000,sep='\001')


#每天增量导出csv
def cdc_to_csv():
    
    html_key=db_query("select max(html_key) from cdc.t_gg",dbtype="postgresql",conp=["postgres","since2015","192.168.4.174","biaost","cdc"]).iat[0,0]
    print("html_key : %d"%html_key)
    conp=["gpadmin","since2015",'192.168.4.179',"base_db","v2"]
    bgdate=datetime.strftime(datetime.now()-timedelta(days=30),'%Y-%m-%d')
    bgdate1=datetime.strftime(datetime.now()-timedelta(days=30),'%Y%m%d')
    eddate=datetime.strftime(datetime.now()+timedelta(days=365),'%Y-%m-%d')
    sql="select distinct on(html_key) * from v2.t_gg where ggstart_time>='%s' and ggstart_time<'%s' and html_key>%d "%(bgdate,eddate,html_key)
    print(sql)
    path="D:/webroot/bstdata/base_cdc_%s.csv"%bgdate1
    pg2csv(sql,conp,path,1000,sep='\001')

#增量csv入库
def csv_to_db_cdc(csvpath,conp,**krg):
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

def insert_t_gg(conp):

    sql="insert into cdc.t_gg select * from cdc.t_gg_tmp"
    db_command(sql,dbtype="postgresql",conp=conp)

def delete_t_gg(conp):
    bgdate=datetime.strftime(datetime.now()-timedelta(days=30),'%Y-%m-%d')
    eddate=datetime.strftime(datetime.now()-timedelta(days=29),'%Y-%m-%d')
    sql="delete from cdc.t_gg where ggstart_time>='%s' and ggstart_time<'%s' "%(bgdate,eddate)
    print(sql)
    db_command(sql,dbtype="postgresql",conp=conp)
# csvpath="D:/webroot/bstdata/base_20190421.csv"
# conp=["postgres","since2015",'192.168.4.174','biaost','cdc'] 

# csv_to_db(csvpath,conp)

#csvpath="D:/webroot/bstdata/base_cdc_20190421.csv"
#conp=["postgres","since2015",'192.168.4.174','biaost','cdc'] 

#csv_to_db_cdc(csvpath,conp)

#快速增量更新
def update_fast():
    print("一、导出增量csv")
    cdc_to_csv()
    files=os.listdir("D:/webroot/bstdata")
    for file in files:
        if file.startswith('base_cdc'):
            name=file
            break
    csvpath="D:/webroot/bstdata/%s"%name
    print(csvpath)
    conp=["postgres","since2015",'192.168.4.174','biaost','cdc'] 
    print("二、csv写入 t_gg_tmp")
    csv_to_db_cdc(csvpath,conp)
    print("三、t_gg_tmp insert into t_gg")
    insert_t_gg(conp=conp)

    print("四、删除回滚的一天")

    delete_t_gg(conp)


#外部环境更新
def update_general(conp):
    bgdate1=datetime.strftime(datetime.now()-timedelta(days=30),'%Y%m%d')
    url_file="http://192.168.4.188/bstdata/base_cdc_%s.csv"%bgdate1
    print("一、下载文件")
    if not os.path.exists("d:/bsttmp"):
        os.mkdir("d:/bsttmp")
    csvpath="d:/bsttmp/base_cdc_%s.csv"%bgdate1
    r = requests.get(url_file, stream=True)
    f = open(csvpath, "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
    f.close()
    print("二、csv写入 t_gg_tmp")
    csv_to_db_cdc(csvpath,conp)
    print("三、t_gg_tmp insert into t_gg")
    insert_t_gg(conp=conp)
    print("四、删除回滚的一天")

    delete_t_gg(conp)

#update_fast()
# cdc_to_csv()
# conp=["postgres","since2015",'192.168.4.174','biaost','cdc'] 
# update_general(conp)

def baseinit(conp,**krg):
    bgdate1=datetime.strftime(datetime.now()-timedelta(days=30),'%Y%m%d')
    url_file="http://192.168.4.188/bstdata/base_%s.csv"%bgdate1
    print("一、下载文件")
    if not os.path.exists("d:/bsttmp"):
        os.mkdir("d:/bsttmp")
    csvpath="d:/bsttmp/base_%s.csv"%bgdate1
    r = requests.get(url_file, stream=True)
    f = open(csvpath, "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
    f.close()
    print("二、csv写入 t_gg")
    csv_to_db(csvpath,conp,**krg)