import pymongo,requests,json,time,traceback
from bson.json_util import dumps
from apscheduler.schedulers.background import BackgroundScheduler



database_url='218.0.61.197:27017'
database_username='admin'
database_password='ADoDev'
myclient = pymongo.MongoClient("mongodb://"+database_username+":"+database_password+"@"+database_url+"/")
mydb = myclient["deploy_platform_new"]
interface_url='http://218.0.61.197:9010/workerflow_manager/task_runner'


#sched=BlockingScheduler()
sched = BackgroundScheduler()

def data_query(table_name,query):
    chart_config_table = mydb[table_name]
    res = json.loads(dumps(chart_config_table.find(query)))
    return res

def get_interface(url):
    res=requests.get(url).text
    print(res)

def base_task():
    print('基础任务运行中')

def job_class_add(task_class,unit,period,task_name,task_id):
    if task_class=='interval':
        sched.add_job(get_interface,i['task_class'],seconds=trans_second(unit,period),args=[interface_url+'?task_id='+task_id],name=task_name,id=task_id)
    print('添加任务成功：'+task_name+',id:'+task_id)


res=data_query('task_manage',{})

def trans_second(unit,period):
    res=int(period)
    if unit=='minutes':
        res=int(period)*60
    if unit=='hours':
        res=int(period)*60*60
    if unit=='days':
        res=int(period)*60*60*24
    if unit=='weeks':
        res=int(period)*60*60*24*7
    if unit=='months':
        res=int(period)*60*60*24*30
    if unit=='years':
        res=int(period)*60*60*24*365
    return res
for i in res:
    print(i['_id']['$oid'])
    job_class_add(i['task_class'],i['unit'],i['period'],i['task_name'],i['_id']['$oid'])


job_list=[]
add_list=[]
del_list=[]
for i in sched.get_jobs():
    job_list.append((i.id))

sched.add_job(base_task, 'interval', days=1, name='base_task', id='0001')

sched.start()


while(True):
    print('开始查询当前任务列表')
    res = data_query('task_manage', {})
    add_list=[]
    del_list=[]
    for i in res:
        if i['task_class']=='interval':
            add_list.append(i['_id']['$oid'])
            if i['_id']['$oid'] not in job_list:
                job_class_add(i['task_class'], i['unit'], i['period'], i['task_name'], i['_id']['$oid'])
                job_list.append(i['_id']['$oid'])
    del_list=[i for i in job_list if i not in add_list]
    if len(del_list)>0:
        if job_list==del_list:
            job_class_add
        for i in del_list:
            try:
                sched.remove_job(i)
                print('删除任务成功,id:'+i)
            except:
                print("错误："+str(traceback.format_exc()))

    time.sleep(10)