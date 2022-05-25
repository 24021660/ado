from app.package_function.target_manager import api
from app.package_function import org_config
from flask_restplus import Resource
from app.package_function import mydb
from bson.json_util import dumps
import traceback,json
parser=api.parser()

parser.add_argument('config_info', type=dict, required=False, help='软件打包序列号')


@api.route('/target_add')
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
            config_info=parse.get('config_info')
            config_info['class']='custom'
            deploy_config_table = mydb['target_config']
            res = deploy_config_table.insert_one(config_info)
            return [0,str(res)]
        except:
            return [1,traceback.format_exc()]
