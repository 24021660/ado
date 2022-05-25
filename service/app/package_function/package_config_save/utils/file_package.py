import os,traceback,time,json,yaml
from ... import mydb,get_now_time,download_url
from bson.json_util import dumps




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
def soft_package(package_path,images_path,docker_install_path,package_id):
    config_info = mydb['deploy_config'].find_one({'_id': package_id})
    for computer_x in config_info['computer_topo']:
        computer_ip=config_info['computer_topo'][computer_x]['ip']
        package_path_res=package_path+str(package_id)+'/'+computer_ip.replace('.','_')
        os.system('mkdir -p '+package_path_res)
        os.system('cp '+package_path+'setup.py '+package_path+str(package_id))
        for soft_id in config_info['computer_topo'][computer_x]['soft_list']:
            if config_info['computer_topo'][computer_x]['install_docker']!=False:
                os.system('cp -r ' + docker_install_path + ' ' +package_path_res)
            if config_info['computer_topo'][computer_x]['soft_list'][soft_id]['image_name']=='kdb':
                return 'kdb'
            else:
                os.system('cp -r ' + images_path + soft_id + '.tar.gz ' + package_path_res)
        os.chdir(package_path+str(package_id))
        os.system('tar -zcvf ' + computer_ip.replace('.','_') + '.tar.gz ' + computer_ip.replace('.','_'))
        os.system('rm -rf ' + package_path_res)
    os.chdir(package_path)
    query = {'_id': package_id}
    update_str = {'$set': {'update_time': get_now_time(int(time.time())), 'status': '更新完成',
                           'download': download_url + 'project/' + str(package_id) + '.tar.gz'}}
    mydb['deploy_config'].update_one(query,update_str)
    config_file=json.loads(dumps(mydb['deploy_config'].find_one(query)))
    config_file['deploy_topo']={}
    for i in config_file['computer_topo']:
        new_ip = config_file['computer_topo'][i]['ip']
        config_file['deploy_topo'][new_ip] = config_file['computer_topo'][i]
    config_file['computer_topo']=''
    with open(package_path+str(package_id)+ '/deploy_config.yaml', 'w') as config_yaml:
        yaml.dump(config_file, config_yaml)
    os.system('tar -zcvf ' + str(package_id) + '.tar.gz ' + str(package_id))
    os.system('rm -rf ' + package_path + str(package_id))

