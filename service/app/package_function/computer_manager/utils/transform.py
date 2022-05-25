import json,time,requests

'''
'''
def computer_trans(par):
    m={}
    m[par['metric']['instance']]=par['value'][1]
    return m


def computer_name_map(par):
    computer_name={}
    computer_name['computer_name']=par['computer_name']
    computer_name['ip']=par['ip']
    return computer_name

def list_trans_dict(par):
    org_trans={}
    for i in par:
        org_trans = {**org_trans, **i}
    return org_trans


def get_current_target(query):
    now_time = time.time()
    url = 'http://10.1.63.215:9090/api/v1/query?query=' + query + '&time=' + str(now_time) + '&_=1638866803842'
    res = json.loads(requests.get(url).text)['data']['result']
    res = map(computer_trans, res)
    res = list_trans_dict(list(res))
    return res

'''
database_username='admin'
database_password='123456'
database_url='10.1.69.43:27017'
myclient = pymongo.MongoClient("mongodb://"+database_username+":"+database_password+"@"+database_url+"/")
mydb = myclient["deploy_platform"]
computer_manager_table = mydb['computer_manager']
computer_list=json.loads(dumps(computer_manager_table.find()))


res_org={}
query_dict={'cpu_rate':'(1%20-%20avg(irate(node_cpu_seconds_total%7Bmode%3D%22idle%22%7D%5B5m%5D))%20by%20(instance))*100','memory_rate':'(1-node_memory_MemAvailable_bytes{}/node_memory_MemTotal_bytes{}) * 100','disk_rate':"(1-(sum(node_filesystem_free_bytes{fstype=~'ext4|xfs'}) by (instance) / sum(node_filesystem_size_bytes{fstype=~'ext4|xfs'}) by (instance)))*100"}
for target_name in query_dict:
    res_org[target_name]=get_current_target(query_dict[target_name])

print(res_org)
computer_name_list=list(map(computer_name_map,computer_list))

res_trans=[]
for i in computer_name_list:
    res_info = {'name': '', 'cpu_rate': '', 'memory_rate': '', 'disk_rate': ''}
    res_info['name'] = i['computer_name']
    res_info['ip'] = i['ip']
    for target_name in query_dict:
        res_info[target_name] = res_org[target_name][i['computer_name']]
    res_trans.append(res_info)




print(res_trans)'''