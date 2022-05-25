from app.package_function.target_manager import api
from app.package_function import org_config
from flask_restplus import Resource
from app.package_function import mydb
from bson.json_util import dumps
from bson import ObjectId
import traceback,json
parser=api.parser()

parser.add_argument('chart_info', type=dict, required=False, help='软件打包序列号')


@api.route('/chart_add')
class BusinessDetails(Resource):
    # 添加接口描述
    @api.doc(description="打包数据打包完成返回0，文件复制未完成返回1")
    @api.expect(parser)
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    # 指定HTTP⽅法
    def post(self): #获取list
        parse = parser.parse_args()
        query_del=[]
        try:
            chart_info=parse.get('chart_info')
            add_data=chart_info['add_data']
            edit_data=chart_info['edit_data']
            del_data=chart_info['del_data']
            chart_config_table = mydb['chart_config']
            for edit_info in edit_data:
                query={'_id':ObjectId(edit_info['_id']['$oid'])}
                edit_set=edit_info
                del edit_set['_id']
                chart_config_table.update_one(query,{'$set':edit_set})
            for del_info in del_data:
                query_del.append({'_id':ObjectId(del_info['_id']['$oid'])})
            chart_config_table.insert_many(add_data)
            chart_config_table.delete_many(query_del)
            return [0,'ok']
        except:
            return [1,traceback.format_exc()]
