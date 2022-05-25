from app.package_function.base_function import api
from app.package_function.base_function.utils import base_function
from flask_restplus import Resource
import traceback
parser=api.parser()

parser.add_argument('table', type=str, required=False, help='表名')
parser.add_argument('query', type=dict, required=False, help='查询语句',default={})


@api.route('/dataquery')
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
            query=parse.get('query')
            table_name=parse.get('table')
            res=base_function.data_query(table_name,query)
            return [0,res]
        except:
            return [1,traceback.format_exc()]
