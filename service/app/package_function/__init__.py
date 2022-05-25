import pymongo,yaml,os,time,redis

with open('/home/project/deploy_config_org.yaml','r') as f:
    org_config=yaml.load(f,Loader=yaml.SafeLoader)

#################mongodb连接####################
database_url=org_config['package_config']['database_url']
database_username=org_config['package_config']['database_username']
database_password=org_config['package_config']['database_password']
myclient = pymongo.MongoClient("mongodb://"+database_username+":"+database_password+"@"+database_url+"/")
mydb = myclient["deploy_platform"]


#################redis连接#######################
redis_info=org_config['database']['redis']
redis_url=redis_info['ip']
redis_port=redis_info['port']
redis_password=redis_info['password']
pool = redis.ConnectionPool(host=redis_url, port=redis_port,password=redis_password,decode_responses=True)
redis_client = redis.Redis(connection_pool=pool)

path=org_config['path']
base_path=path['base_path']
org_config_table=mydb['org_config']
query={'org_class':'deploy_config_org'}
if org_config_table.find(query).count()>0:
    org_config_table.update_one(query,{'$set':org_config})
else:
    org_config_table.insert_one(org_config)
#org_config_table.insert_one({'package_config': {'database_url': '10.1.69.43:27017', 'database_username': 'admin', 'database_password': '123456', 'deploy_platform_file_path': {'path': '/home/ssd/deploy_platform', 'deploy_config': 'deploy_platform_config', 'dockerfile': 'dockerfile', 'images': 'file/images', 'docker_install': 'file/system/centos/docker/7'}, 'package_file_path': {'path': '/home/ssd/deploy_file'}}, 'deploy_config': {'version_no': '1_0', 'product_name': 'aiops', 'project_no': '001', 'project_topo': [{'ip': '10.1.1.1', 'soft_list': ['redis', 'nginx', 'aiops_core']}, {'ip': '10.1.1.2', 'soft_list': ['aiops_handler', 'kdb']}], 'images_config': {'aiops_ai': {'v': ['aiops_ai:/home/eb_aiops_flask'], 'p': ['8030:8080']}, 'aiops_core': {'v': ['aiops_core:/home/eb_aiops_flask'], 'p': ['8040:8080']}, 'aiops_handler': {'v': ['aiops_handler:/home/eb_aiops_flask'], 'p': ['8020:8080']}, 'cassandra': {'v': '', 'p': ['9042:9042']}, 'kdb': {'v': '', 'p': ['8010:8080']}, 'mongo': {'v': '', 'p': ['27017:27017']}, 'redis': {'v': '', 'p': ['6379:6379']}, 'nginx': {'v': ['aiops_web:/usr/share/nginx/html'], 'p': ['8050:80']}, 'aiops_collector': {'v': 'aiops_collector:/home/project', 'p': ''}}, 'container_start_num': {1: ['cassandra', 'mongo', 'kdb', 'redis'], 2: ['aiops_ai', 'aiops_core', 'aiops_handler', 'nginx'], 3: ['aiops_collector']}}})


deploy_path=org_config['package_config']['deploy_platform_file_path']
dockerfile_path=path['base_path']+path['dockerfile_path']
images_path=path['base_path']+path['images_path']


#######开启定时任务###########
os.system('python3 /home/project/app/cron/main.py')

def get_dict_key(input_data):
    res=[]
    for dict_key in input_data:
        res.append(dict_key)
    return res

def get_now_time(now_timestamp):
    timeArray = time.localtime(now_timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


log_path='/home/dockerfile_log/'
dockerfile_tar_path='/home/dockerfile_tar/'
dockerfile_path='/home/dockerfile/'
images_path='/home/deploy_file/images/'
package_path='/home/deploy_file/project/'
docker_install_path='/home/deploy_file/docker'
download_url='http://10.1.69.43:9010/'