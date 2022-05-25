import requests,os,json,yaml
import redis


base_url='/Users/chenchen/PycharmProjects/deploy_platform/'
def test2():
    insert_url='http://10.1.69.4:9010/api/v1/datapoints'
    metric_name='aiops.target.host.value'
    headers={'Authorization': 'Basic dGVzdDoxMjM0NQ=='}
    insert_data=[{"name": metric_name, "datapoints": [[1638579600000, 999]],
                         "tags": {'ip':'10.228.103.168','target_name':'cpu_rate'}, "ttl": 0
                         }]

    data_target = requests.post(insert_url, headers=headers,data=str(insert_data).encode())

    print(data_target.text)

def redis_target(target_name):
    res=os.popen("redis-cli -h 10.1.69.43 -p 6379 -a 123456 info |grep -w 'blocked_clients'")
    print(res.read())


def file_folder_exist(path):
    return os.path.exists(path)

def create_prom_config_file(metric_url,config_class,instance_name):
    config_file_path='../../prometheus/' + config_class
    config_json='[{"targets": ["'+metric_url+'"],"labels": {"instance": "'+instance_name+'"}}]'
    if file_folder_exist(config_file_path)==False:
        os.mkdir(config_file_path)
    with open(config_file_path+'/'+instance_name+'.json','w') as f:
        f.write(config_json)

#print(file_folder_exist('../../prometheus/node_exporter'))

#create_prom_config_file('10.1.62.158:9100','node_exporter','test1')

def init_prom():
    prom_str={'global': {'scrape_interval': '15s', 'evaluation_interval': '15s'}, 'alerting': {'alertmanagers': [{'static_configs': [{'targets': None}]}]}, 'rule_files': None, 'scrape_configs': [{'job_name': 'node_exporter', 'metrics_path': '/metrics', 'file_sd_configs': [{'refresh_interval': '1m', 'files': ['/data/prom_config/node_exporter/*.json']}]}]}
    with open('../../prometheus/promethus.yml', 'w') as f:
        yaml.dump(prom_str,f)


def redis_test():
    with open(base_url+'deploy_config_org.yaml', 'r') as f:
        org_config = yaml.load(f, Loader=yaml.SafeLoader)
    redis_info = org_config['database']['redis']
    redis_url = redis_info['ip']
    redis_port = redis_info['port']
    redis_password = redis_info['password']
    pool = redis.ConnectionPool(host=redis_url, port=redis_port, password=redis_password, decode_responses=True)
    redis_client = redis.Redis(connection_pool=pool)
    redis_client.hset('host_status','10.1.69.43','123')
    redis_client.hset('host_status', '10.1.69.158', 'none')
    m=redis_client.hgetall('host_status')
    redis_client.rpush('host_list', '10.1.69.43')
    n=redis_client.lrange('host_list',0,-1)
    print(m)
    print(n)

redis_test()