import pymongo,json,os,yaml,requests,time
from bson.json_util import dumps
from bson import ObjectId
import csv
myclient = pymongo.MongoClient("mongodb://admin:123456@10.1.69.43:27017/")
mydb = myclient["deploy_platform"]


test_table=mydb['target_manager']
chart_table=mydb['chart_manager']
query={}
m=60*60
time_now=int(time.time()/3600)*3600
time_start=time_now-m*int(1)

def get1(c):
    return c[0]
def get2(c):
    return c[1]

def get_now_time(now_timestamp):
    timeArray = time.localtime(now_timestamp)
    otherStyleTime = time.strftime("%H:%M:%S", timeArray)
    return otherStyleTime
def test():
    chart_info_dict={"_id": {"$oid": 'echarts'}, 'chart_name': '主机指标','data_label':[],'data':[]}
    for target_info in config_file:
        query=target_info['query_name']
        url='http://10.1.63.215:9090/api/v1/query_range?query='+query+'&start='+str(time_start)+'&end='+str(time_now)+'&step='+str(m)+'&_=1638260133788'
        res=requests.get(url)
        for i in json.loads(res.text)['data']['result']:
            print(i)
            chart_info_dict['time_array']=list(map(get_now_time,map(get1,i['values'])))
            chart_info_dict['data_label'].append(i['metric']['instance']+'_'+target_info['target_name'])
            chart_info_dict['data'].append({'name':i['metric']['instance']+'_'+target_info['target_name'],'type':'line','data':list(map(get2,i['values']))})

    print(chart_info_dict)

def csv_load():
    title=['序号', '类别', '类别英文名', '一级分类', '二级分类', '指标名称', '指标英文名', '指标级别', '指标单位', '指标模型', '指标粒度', '采集语句', '数据来源', '所属进程', '']
    example2={
    "chart_name": "cpu使用率",
    "time_range": "60",
    "time_class": "m",
    "unit_class": "百分比"
    }
    res_list=[]
    chart_list=[]
    with open('./123.csv','r') as f:
        res=csv.reader(f)
        for res_info in res:
            example = {
            }
            example2={}
            example['target_class']=res_info[3]
            example['target_second_class']=res_info[4]
            example['target_name']=res_info[5]
            example['target_english_name']=res_info[6]
            example['query_name']=res_info[11]
            if res_info[8]=='%':
                example['target_unit']='百分比'
                example2['unit_class']='百分比'
            else:
                example['target_unit']=res_info[8]
                example2['unit_class']='百分比'
            example['table_name']=res_info[5]
            example2['chart_name']=res_info[5]
            example2['time_range']='60'
            example2['time_class']='m'
            res_list.append(example)
            chart_list.append(example2)
    test_table.insert_many(res_list)
    chart_table.insert_many(chart_list)
def del_all():
    test_table.delete_many({})
    chart_table.delete_many({})

def is_ok():
    res=test_table.find()
    for res_info in res:
        id=res_info['_id']
        query=str(res_info['query_name']).replace('{','%7B').replace('}','%7D').replace(' ','%20').replace('[','%5B').replace(']','%5D').replace('+','%2B')
        print(query)
        url = 'http://10.1.63.215:9090/api/v1/query_range?query=' + query + '&start=' + str(
            time_start) + '&end=' + str(time_now) + '&step=' + str(m) + '&_=1638260133788'
        print(url)
        res = requests.get(url)
        print(res.text)

#del_all()
#csv_load()
is_ok()