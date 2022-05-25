from .utils import file_package
from . import api
from flask_restplus import Resource
from app.package_function import mydb,org_config

parser=api.parser()

parser.add_argument('package_no', type=str, required=True, help='软件打包序列号')


@api.route('/package')
class BusinessDetails(Resource):
    # 添加接口描述
    @api.doc(description="打包数据打包完成返回0，文件复制未完成返回1")
    @api.expect(parser)
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    # 指定HTTP⽅法
    def post(self):
        parse = parser.parse_args()
        deploy_config_table = mydb['deploy_config']
        package_no = parse.get('package_no')
        deploy_path=org_config['package_config']['deploy_platform_file_path']
        package_path=org_config['package_config']['package_file_path']['path']
        config_info=file_package.get_config_info(package_no,deploy_config_table)
        res=file_package.soft_package(deploy_path,package_path,config_info['project_topo'],config_info['project_no'],config_info['project_version'],config_info['product_name'])
        return res


