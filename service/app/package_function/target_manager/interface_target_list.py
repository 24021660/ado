from app.package_function.target_manager import api
from flask_restplus import Resource
from app.package_function import mydb
from bson.json_util import dumps
import traceback,json
parser=api.parser()


@api.route('/target_add')
class BusinessDetails(Resource):
    # 添加接口描述
    @api.doc(description="打包数据打包完成返回0，文件复制未完成返回1")
    @api.expect(parser)
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    # 指定HTTP⽅法
    def get(self): #获取list
        try:
            deploy_config_table = mydb['target_config']
            query={'class':'custom'}
            res = json.loads(dumps(deploy_config_table.find(query)))
            return [0,res]
        except:
            return [1,traceback.format_exc()]
