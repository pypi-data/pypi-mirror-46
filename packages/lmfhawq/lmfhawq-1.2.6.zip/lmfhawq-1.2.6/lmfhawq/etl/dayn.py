from lmf.dbv2 import db_command ,db_query 
import time 
import traceback
def add_days(date1,date2,conp):
    #date1,date2='2019-04-01','2019-05-13'
    #conp=["gpadmin","since2015",'192.168.4.179','base_db','etl']
    sql="select partitionname from pg_partitions where schemaname='v' and tablename='gg_html' order by partitionname"
    df=db_query(sql,dbtype="postgresql",conp=conp)
    arr=df['partitionname'].values
    for w in arr:
        try:
            bg=time.time()
            quyu=w
            print(w)
            sql="select etl.add_quyu_days('%s','%s','%s')"%(date1,date2,quyu)
            
            db_command(sql,dbtype='postgresql',conp=conp)
            ed=time.time()
            cost=int(ed-bg)
            print(sql,'耗时%d秒'%cost)
        except:
            traceback.print_exc()


#add_days('2019-04-01','2019-05-13',conp=["gpadmin","since2015",'192.168.4.179','base_db','etl'])


