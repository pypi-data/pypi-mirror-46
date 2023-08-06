from lmfhawq.etl.app import update_general ,update_tb1


def task():
    conp=['postgres','zhulong.com.cn','192.168.169.47','biaost','cdc']
    update_general(conp=conp)

    update_tb1(conp=conp)