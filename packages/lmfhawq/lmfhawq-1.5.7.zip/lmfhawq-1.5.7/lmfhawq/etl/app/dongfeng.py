from lmfhawq.etl.app import update_general ,update_tb1


def task():
    conp=['postgres','since2015','192.168.3.172','biaost','cdc']
    update_general(conp=conp)

    update_tb1(conp=conp)