from app.package_function.docker_image_manage import api
from app.package_function import org_config
from flask_restplus import Resource
from app.package_function import mydb,org_config
import os,traceback,time
from .. import get_now_time,dockerfile_path,images_path,dockerfile_tar_path,download_url
from .utils import images_update

parser=api.parser()

parser.add_argument('dockerfile_id', type=dict, required=True, help='dockerfile名称')



@api.route('/docker_images_update')
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
            dockerfile_id=parse.get('dockerfile_id')
            res=images_update.update_image(dockerfile_id)
            return res
        except:
            return [1,traceback.format_exc()]



