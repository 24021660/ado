import paramiko


'''
###########测试ssh远程连接###########
function name：ssh_host
参数：
    host_name:主机ip
    port:ssh端口
    username:用户名
    password:密码
'''
def ssh_host_check(hostname,port,username,password):
    ssh=paramiko.SSHClient()
    know_host=paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(know_host)
    try:
        ssh.connect(hostname=hostname,port=port,username=username,password=password)
        ssh.exec_command('mkdir /data')
        ssh.close()
        return 0
    except :
        return 1



'''
###########ssh远程连接，并执行command命令###########
function name：ssh_host
参数：
    host_name:主机ip
    port:ssh端口
    username:用户名
    password:密码
    command:命令行
'''
def ssh_host(hostname,port,username,password,command):
    ssh=paramiko.SSHClient()
    know_host=paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(know_host)

    ssh.connect(hostname=hostname,port=port,username=username,password=password)

    stdin,stdout,stderr=ssh.exec_command(command)

    print(stdout.read().decode())
    stdin.close()
    ssh.close()




def ssh_cp_file(ip,port,username,password,local_path,file_name,remote_path):
    #检查该ip下是否有salt


    #复制文件到指定机器
    scp = paramiko.Transport((ip, port))
    scp.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(scp)
    try:
        local_file = local_path + file_name
        remote_file = remote_path + file_name
        sftp.put(local_file, remote_file)
    except IOError:  # 如果目录不存在则抛出异常
        return ("remote_path or local_path is not exist")
    scp.close()
    return 0

#salt_minion_install('10.1.62.158',19222,'root','EBupt!@#123','/Users/chenchen/test/','/root/')
