from app.package_function.computer_manager import api
from app.package_function.base_function.utils import base_function
from flask_restplus import Resource
from app.package_function.computer_manager.utils import host_ssh,install_monitor_agent,promethus
import traceback
parser=api.parser()

parser.add_argument('table', type=str, required=False, help='表名')
parser.add_argument('ssh_info', type=dict, required=False, help='查询语句',default={})


@api.route('/ssh_check')
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
            table_name=parse.get('table')
            ssh_info=parse.get('ssh_info')
            host_ip=ssh_info['ip']
            host_port=int(ssh_info['ssh_port'])
            username=ssh_info['ssh_username']
            password=ssh_info['ssh_password']
            ssh_info['node_exporter']='installing'
            check_res=host_ssh.ssh_host_check(host_ip,host_port,username,password)
            if check_res==0:
                base_function.redis_commit_list('host_list',host_ip)
                base_function.data_commit(table_name,ssh_info)
                install_monitor_agent.install_node_exporter(ssh_info)
                promethus.create_prom_config_file(host_ip+':9100','node_exporter',ssh_info['computer_name'])
            return [0,check_res]

        except:
            return [1,traceback.format_exc()]
