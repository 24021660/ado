from app.package_function.computer_manager import api
from app.package_function.base_function.utils import base_function
from flask_restplus import Resource
from app.package_function.computer_manager.utils import host_alive
import traceback
parser=api.parser()


@api.route('/host_ping_alive')
class BusinessDetails(Resource):
    # 添加接口描述
    @api.doc(description="打包数据打包完成返回0，文件复制未完成返回1")
    @api.expect(parser)
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    # 指定HTTP⽅法
    def get(self): #获取list
        try:
            host_alive.ping_host_list()
            return [0,'ok']
        except:
            return [1,traceback.format_exc()]
