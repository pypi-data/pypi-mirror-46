import lmfhawq.zl as src 

import lmfhawq.zldb as v 

from lmfhawq.data import zhulong_diqu_dict


src_add_quyu=src.add_quyu_fast 


src_drop_quyu=src.drop_quyu_fast


src_add_quyu1=src.add_quyu_fast1 


src_drop_quyu1=src.drop_quyu_fast1

src_add_quyu1=src.add_quyu_fast2


src_drop_quyu1=src.drop_quyu_fast2


v_add_quyu=v.add_quyu 

v_drop_quyu=v.drop_quyu 


v_add_quyu1=v.add_quyu1 

v_drop_quyu1=v.drop_quyu1 



def src_add_sheng(sheng,tag):
    quyus=zhulong_diqu_dict['sheng']
    for quyu in quyus:

        src_add_quyu(quyu,tag)

def v_add_sheng(sheng,tag):
    quyus=zhulong_diqu_dict['sheng']
    for quyu in quyus:

        v_add_quyu(quyu,tag)




