from app.package_function.base_function import api
from app.package_function.base_function.utils import base_function
from flask_restplus import Resource
import traceback
parser=api.parser()

parser.add_argument('table', type=str, required=False, help='表名')
parser.add_argument('commit_data', type=dict, required=False, help='查询语句',default={})

@api.route('/datacommit')
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
            commit_data = parse.get('commit_data')
            table_name = parse.get('table')
            base_function.data_commit(table_name,commit_data)
            return [0, 'ok']
        except:
            return [1, traceback.format_exc()]
