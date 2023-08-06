from . import gcjs,ggzy,zfcg,qycg

def write_all(dirname,**krg):
    ggzy.write_dags(dirname,**krg)

    zfcg.write_dags(dirname,**krg)

    gcjs.write_dags(dirname,**krg)

    qycg.write_dags(dirname,**krg)
