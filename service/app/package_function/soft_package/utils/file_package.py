import os,traceback

import yaml




###########获取拓扑结构#############
def get_config_info(package_no,config_table):
    config_info=config_table.find_one({'package_no':package_no})
    return config_info


#########kdb打包###################
def kdb_image_create(deploy_path,package_path,product_name,project_no,project_version,computer_ip):
    base_path=deploy_path['path']
    dockerfile_path=base_path+'/'+deploy_path['dockerfile']
    images_path=base_path+'/'+deploy_path['images']
    os.chdir(dockerfile_path+'/kdb')
    os.system('cp -r '+images_path+'/cassandra_image '+package_path+'/' + product_name + '/' + project_no + '/' + project_version + '/ip_' + computer_ip + '/images/cassandra_image')
    with open(dockerfile_path+'/kdb/kairosdb_org.properties', 'r') as p:
        kdb_conf = p.readlines()
    with open(dockerfile_path+'/kdb/kairosdb.properties', 'w') as f:
        for conf_text in kdb_conf:
            if conf_text.find('kairosdb.datastore.cassandra.cql_host_list') != -1:
                conf_text = 'kairosdb.datastore.cassandra.cql_host_list=' + computer_ip + '\n'
            f.write(conf_text)
    os.system('docker build -t kdb .')
    os.system('docker save kdb -o '+images_path+'/kdb_image ')
    os.system('docker rmi $(docker images | grep "none" | awk \'{print $3}\')')




##########docker安装包打包##########
#线下
def soft_package(deploy_path,package_path,project_topo,project_no,project_version,product_name):
    base_path = deploy_path['path']
    images_path = base_path + '/' + deploy_path['images']
    docker_install_path=base_path+'/'+deploy_path['docker_install']
    try:
        for computer in project_topo:
            computer_ip=computer['ip'].replace('.','_')
            if os.path.exists(package_path+product_name+'/'+project_no+'/'+project_version+'/ip_'+computer_ip)==False:
                os.system('mkdir -p '+package_path+product_name+'/'+project_no+'/'+project_version+'/ip_'+computer_ip+'/images')
            #if os.path.exists('/home/ssd/deploy_file/'+product_name+'/package_file/'+project_no)==False:
                #os.system('mkdir -p /home/ssd/deploy_file/' + product_name + '/package_file/' + project_no)
            os.system('cp -r '+docker_install_path+' '+package_path+product_name+'/'+project_no+'/'+project_version+'/ip_'+computer_ip+'/docker')
            for soft_name in computer['soft_list']:
                if soft_name=='kdb':
                    kdb_image_create(deploy_path,package_path,product_name,project_no,project_version,computer_ip)
                try:
                    os.system('cp -r '+images_path+'/'+soft_name+'_image '+package_path + product_name + '/' + project_no + '/' + project_version + '/ip_' + computer_ip + '/images/'+soft_name+'_image')
                except:
                    print(soft_name+'此文件不存在')
            os.chdir(package_path + product_name + '/' + project_no + '/' + project_version)
            os.system('tar -zcvf ' +computer_ip+'.tar.gz '+package_path + product_name + '/' + project_no + '/' + project_version+'/ip_'+computer_ip)
            os.system('rm -rf '+package_path + product_name + '/' + project_no + '/' + project_version+'/ip_'+computer_ip)
        ##########文件打包################
        os.chdir(package_path + product_name + '/' + project_no)
        os.system('cp')
        os.system('tar -zcvf '+ project_version+'.tar.gz '+package_path + product_name + '/' + project_no + '/' + project_version)
        os.system('rm -rf '+package_path + product_name + '/' + project_no + '/' + project_version)
        return [0,'ok']
    except:
        return [1,traceback.format_exc()]


