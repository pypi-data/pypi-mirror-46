import paramiko

def exe_on_remote(cmd,con):
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    host,user,password=con
    ssh.connect(hostname=host, port=22, username=user, password=password)

    #cmd="""/opt/python35/bin/python3 -c "from lmfhawq.zl import add_quyu_fast;add_quyu_fast('anhui_chuzhou')" """
    stdin, stdout, stderr = ssh.exec_command(cmd,timeout=100)

    result = stdout.read()
    print(result.decode())

    print(stderr.read().decode())

    ssh.close()


#ssh.connect(hostname='192.168.4.187', port=22, username='root', password='rootHDPHAWQDatanode5@zhulong')
