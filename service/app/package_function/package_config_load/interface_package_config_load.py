from app.package_function.package_config_save import api
from app.package_function import org_config
from flask_restplus import Resource
from app.package_function import mydb
from bson.json_util import dumps
import traceback,json
parser=api.parser()

parser.add_argument('package_no', type=dict, required=False, help='软件打包序列号')
parser.add_argument('product_version',type=str, required=False, help='软件打包序列号',default='all')
parser.add_argument('product_name',type=str, required=False, help='软件打包序列号',default='all')
parser.add_argument('product_no',type=str, required=False, help='软件打包序列号',default='all')


@api.route('/package_config_load')
class BusinessDetails(Resource):
    # 添加接口描述
    @api.doc(description="打包数据打包完成返回0，文件复制未完成返回1")
    @api.expect(parser)
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    # 指定HTTP⽅法
    def get(self): #获取list
        parse = parser.parse_args()
        try:
            query={}
            product_version=parse.get('product_version')
            product_name = parse.get('product_name')
            product_no = parse.get('product_no')
            if(product_no!='all'):
                query['product_no']=product_no
            if (product_name != 'all'):
                query['product_name'] = product_name
            if (product_version != 'all'):
                query['product_version'] = product_version
            deploy_config_table = mydb['deploy_config']
            res = json.loads(dumps(deploy_config_table.find(query)))
            return [0,res]
        except:
            return [1,traceback.format_exc()]
