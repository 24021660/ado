from app.package_function.target_manager import api
from app.package_function import org_config
from flask_restplus import Resource
from app.package_function import mydb
from bson.json_util import dumps
from bson import ObjectId
import traceback,json,time,requests
from .. import get_now_time
from .utils.getlist import get1,get2,get_now_time
parser=api.parser()

parser.add_argument('query', type=dict, required=False, help='软件打包序列号',default={})


@api.route('/chart_list')
class BusinessDetails(Resource):
    # 添加接口描述
    @api.doc(description="打包数据打包完成返回0，文件复制未完成返回1")
    @api.expect(parser)
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    # 指定HTTP⽅法
    def post(self): #获取list
        parse = parser.parse_args()
        try:
            res_dict = []
            query=parse.get('query')
            chart_config_table = mydb['chart_manager']
            target_config_table=mydb['target_manager']
            res=json.loads(dumps(chart_config_table.find(query)))
            for chart_info in res:
                chart_info_dict={"_id": {"$oid": 'echarts'}, 'chart_name': '主机指标','data_label':[],'data':[]}
                chart_info_dict['_id']=chart_info['_id']
                chart_info_dict['chart_name']=chart_info['chart_name']
                if chart_info['time_class']=='h':
                    m=60*60

                elif chart_info['time_class']=='m':
                    m=60
                time_now = int(time.time() / m) * m
                time_start = time_now - m * int(chart_info['time_range'])
                query_target={'table_name':chart_info_dict['chart_name']}
                res_target = json.loads(dumps(target_config_table.find(query_target)))
                for target_info in res_target:
                    query = target_info['query_name'].replace('{','%7B').replace('}','%7D').replace(' ','%20').replace('[','%5B').replace(']','%5D').replace('+','%2B')
                    url = 'http://10.1.63.215:9090/api/v1/query_range?query=' + query + '&start=' + str(
                        time_start) + '&end=' + str(time_now) + '&step=' + str(m) + '&_=1638866803815'
                    res = requests.get(url)
                    for i in json.loads(res.text)['data']['result']:
                        if len(i)>0:
                            chart_info_dict['time_array'] = list(map(get_now_time,map(get1, i['values'])))
                            chart_info_dict['data_label'].append(i['metric']['instance'] + '_' + target_info['target_name'])
                            chart_info_dict['data'].append(
                                {'name': i['metric']['instance'] + '_' + target_info['target_name'], 'type': 'line',
                                 'data': list(map(get2, i['values']))})
                res_dict.append(chart_info_dict)
                print(res_dict)
            return [0,res_dict]
        except:
            return [1,traceback.format_exc()]
