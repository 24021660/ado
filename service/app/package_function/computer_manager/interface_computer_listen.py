from app.package_function.computer_manager import api
from flask_restplus import Resource
from app.package_function import mydb
from bson.json_util import dumps
import traceback,json
from .utils.transform import computer_name_map
from .utils.promethus import get_current_target


parser=api.parser()

parser.add_argument('table', type=str, required=False, help='表名')
parser.add_argument('commit_data', type=dict, required=False, help='查询语句',default={})

@api.route('/computer_listen')
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
            res_org = {}
            computer_manager_table = mydb['computer_manager']
            computer_list = json.loads(dumps(computer_manager_table.find()))
            query_dict = {
                'cpu_rate': '(1%20-%20avg(irate(node_cpu_seconds_total%7Bmode%3D%22idle%22%7D%5B5m%5D))%20by%20(instance))*100',
                'memory_rate': '(1-node_memory_MemAvailable_bytes{}/node_memory_MemTotal_bytes{}) * 100',
                'disk_rate': "(1-(sum(node_filesystem_free_bytes{fstype=~'ext4|xfs'}) by (instance) / sum(node_filesystem_size_bytes{fstype=~'ext4|xfs'}) by (instance)))*100"}
            for target_name in query_dict:
                res_org[target_name] = get_current_target(query_dict[target_name])

            print(res_org)
            computer_name_list = list(map(computer_name_map, computer_list))

            res_trans = []
            for i in computer_name_list:
                res_info = {'name': '', 'cpu_rate': '', 'memory_rate': '', 'disk_rate': ''}
                res_info['name'] = i['computer_name']
                res_info['ip']=i['ip']
                for target_name in query_dict:
                    res_info[target_name] = res_org[target_name][i['computer_name']][:4]+'%'
                res_trans.append(res_info)
            return [0, res_trans]
        except:
            return [1, traceback.format_exc()]
