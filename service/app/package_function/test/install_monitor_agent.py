import host_ssh


def install_node_exporter(query):
    host_ip = query['ip']
    host_port = int(query['ssh_port'])
    username = query['ssh_username']
    password = query['ssh_password']
    remote_path=query['ssh_path']
    local_path='/home/project/app/agent/'
    local_path='../../agent/'
    file_name='node_exporter-1.3.1.linux-amd64.tar.gz'
    if remote_path[-1]!='/':
        remote_path+='/'
    command='cd /data;tar -zxvf node_exporter-1.3.1.linux-amd64.tar.gz;cd node_exporter-1.3.1.linux-amd64;ls;./node_exporter > /dev/null 2>&1 &'
    host_ssh.ssh_cp_file(host_ip,host_port,username,password,local_path,file_name,remote_path)
    host_ssh.ssh_host(host_ip,host_port,username,password,command)


query={
    "_id": {
        "$oid": "61b06280a59e8a847c22f65a"
    },
    "edit_class": "edit",
    "computer_name": "database",
    "ip": "10.1.62.158",
    "ssh_username": "root",
    "ssh_password": "EBupt!@#123",
    "ssh_port": "19222",
    "ssh_path": "/data"
}
#install_node_exporter(query)

