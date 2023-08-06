from lmf.dbv2 import db_command ,db_query 
import time 
import traceback
import os 




def t_gg():
    #
    conp=["gpadmin","since2015",'192.168.4.179',"base_db","v2"]
    path=os.path.join(os.path.dirname(__file__),'key.txt')


    with open(path,'r') as f:
        lines=f.readlines()
    gg_key,html_key=[ int(w.strip()) for w in lines]




    ##写入tmp表
    sql1="""
    drop table if exists v2.tmp
    ;

    select distinct on (gg_key) a.*,b.html_key,b.page into v2.tmp from 
     ( select * from v.gg where gg_key>%d) as a,
    (select * from v.gg_html where html_key>%d) as  b 
    where a.href=b.href  and a.quyu=b.quyu 
    """%(gg_key,html_key)

    print("一、写入v2.tmp表")
    print(sql1)

    db_command(sql1,dbtype="postgresql",conp=conp)



    sql2="""
    insert into v2.t_gg 

    select * from v2.tmp 
    """
    print("二、插入v2.t_gg")
    print(sql2)
    db_command(sql2,dbtype="postgresql",conp=conp)


    ##235秒查出key
    sql3="""
    select max(gg_key) gg_key,max(html_key) html_key from v2.tmp
    """
    print("三、查出最大gg_key html_key 预计耗时235秒")
    print(sql3)
    df=db_query(sql3,dbtype="postgresql",conp=conp)

    gg_key,html_key=df.values.tolist()[0]
    if gg_key is None:
        sql3="""
        select max(gg_key) gg_key,max(html_key) html_key from v2.t_gg
        """
        print("三、查出最大gg_key html_key 预计耗时235秒")
        print(sql3)
        df=db_query(sql3,dbtype="postgresql",conp=conp)

        gg_key,html_key=df.values.tolist()[0]
    print(gg_key,html_key)
    with open(path,'w') as f :
        f.write(str(gg_key)+"\n")
        f.write(str(html_key))



#t_gg()