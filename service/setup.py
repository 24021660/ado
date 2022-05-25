import os
import yaml

#功能逻辑部分=============================================================================
#初始化数据
#映射
with open('./deploy_config.yaml', 'r') as config_yaml:
    config_dict=yaml.load(config_yaml)

this_computer_ip='127.0.0.1'
version_no=config_dict['deploy_info']['version_no'].replace('.','_')
project_topo=config_dict['deploy_topo']

#获取本机ip地址
def get_this_computer_ip():
    ip_address = os.popen('ifconfig').read()
    for computer_info in project_topo:
        if str(ip_address).find(computer_info['ip']) != -1:
            this_computer_ip=computer_info['ip']
        file_ip_name=this_computer_ip.replace('.','_')
    return file_ip_name

#docker安装
def docker_install(file_name):
    info_list=os.popen('docker ps -a').read()
    print(len(info_list))
    if len(info_list)==0:
        print('该系统没有安装docker，启动docker安装程序')
        os.system('rpm -Uvh ./'+file_name+'/docker/base/*.rpm --nodeps --force')
        os.system('rpm -Uvh ./'+file_name+'/docker/docker/containerd.io-1.4.4-3.1.el7.x86_64.rpm')
        os.system('rpm -Uvh ./'+file_name+'/docker/docker/container-selinux-2.107-3.el7.noarch.rpm')
        os.system('rpm -Uvh ./'+file_name+'/docker/docker/docker-ce-19.03.3-3.el7.x86_64.rpm')
        os.system('rpm -Uvh ./'+file_name+'/docker/docker/docker-ce-cli-18.09.3-3.el7.x86_64.rpm')
        os.system('systemctl start docker')

#镜像安装
def images_load_run(file_ip_name):
    soft_list=os.listdir('./'+file_ip_name)
    port_str =''
    volume_str=''
    for soft_name in soft_list:
        if soft_name =='docker':
            docker_install(file_ip_name)
        else:
            os.chdir('./'+file_ip_name)
            soft_tar_name=soft_name.split('.')[0]
            container_name=config_dict['deploy_topo'][file_ip_name]['soft_list'][soft_tar_name]['image_name']
            port_info=config_dict['deploy_topo'][file_ip_name]['soft_list'][soft_tar_name]['port'].split(' ')
            volume_info=config_dict['deploy_topo'][file_ip_name]['soft_list'][soft_tar_name]['v'].split(' ')
            for port_conf in port_info:
                port_str+='-p '+port_conf+' '
            for volume_conf in volume_info:
                volume_str+='-v '+volume_conf+' '
            load_res=os.popen('docker load <'+soft_name)
            for i in load_res:
                if i.find('Loaded image') != -1:
                    image_name=i[14:]
            os.system('docker run -itd --name '+container_name+'_instance '+port_str+volume_str+image_name)

#运行=============================================================================
#main函数
def main():
    file_ip_name=get_this_computer_ip()
    os.system('tar -zxvf ./'+file_ip_name+'tar.gz')
    images_load_run(file_ip_name)

#运行main函数
#main()