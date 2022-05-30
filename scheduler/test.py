import pymongo,requests,json,time
from bson.json_util import dumps
from apscheduler.schedulers.background import BackgroundScheduler



database_url='218.0.61.197:27017'
database_username='admin'
database_password='ADoDev'
myclient = pymongo.MongoClient("mongodb://"+database_username+":"+database_password+"@"+database_url+"/")
mydb = myclient["deploy_platform_new"]
interface_url='http://218.0.61.197:9010/workerflow_manager/task_runner'

def data_query(table_name,query,colomn={}):
    chart_config_table = mydb[table_name]
    res = json.loads(dumps(chart_config_table.find(query,colomn)))
    return res



res = data_query('task_manage', {},{'_id':0,'isset':1})

print(res)