import requests,time,json,os
from app.package_function.computer_manager.utils import transform
from app.package_function.base_function.utils import base_function
import yaml


test_path='../../../'
normal_path='/home/project/app/'

use_path=normal_path


def init_prom():
    prom_str={'global': {'scrape_interval': '15s', 'evaluation_interval': '15s'}, 'alerting': {'alertmanagers': [{'static_configs': [{'targets': None}]}]}, 'rule_files': None, 'scrape_configs': [{'job_name': 'node_exporter', 'metrics_path': '/metrics', 'file_sd_configs': [{'refresh_interval': '1m', 'files': ['/data/prom_config/node_exporter/*.json']}]}]}
    with open(use_path+'prometheus/prometheus.yml', 'w') as f:
        yaml.dump(prom_str,f)


def get_current_target(query,prom_url='http://10.1.63.215:9090/'):
    now_time = time.time()
    url = prom_url+'api/v1/query?query=' + query + '&time=' + str(now_time) + '&_=1638866803842'
    res = json.loads(requests.get(url).text)['data']['result']
    res = map(transform.computer_trans, res)
    res = transform.list_trans_dict(list(res))
    return res


def create_prom_config_file(metric_url,config_class,instance_name):
    config_file_path=use_path+'prometheus/' + config_class
    config_json='[{"targets": ["'+metric_url+'"],"labels": {"instance": "'+instance_name+'"}}]'
    if base_function.file_folder_exist(config_file_path)==False:
        os.mkdir(config_file_path)
    with open(config_file_path+'/'+instance_name+'.json','w') as f:
        f.write(config_json)

def get_node_exporter_status():
    url='http://10.1.69.43:9090/api/v1/targets?state=active'
    res = json.loads(requests.get(url).text)
    if res['status'] == 'success':
        for i in res['data']['activeTargets']:
            if i['labels']['job']=='node_exporter':
                query = {'computer_name': i['labels']['instance']}
                commit_data = {'node': i['health']}
                base_function.data_update('computer_manager', query, commit_data)

