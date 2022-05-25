from app.package_function.package_config_save import api
from flask_restplus import Resource
from app.package_function import mydb,get_now_time,package_path,images_path,docker_install_path
import time,traceback
from .utils import file_package
parser=api.parser()

parser.add_argument('config_info', type=dict, required=True, help='软件打包序列号')



@api.route('/package_config_save')
class BusinessDetails(Resource):
    # 添加接口描述
    @api.doc(description="打包数据打包完成返回0，文件复制未完成返回1")
    @api.expect(parser)
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    # 指定HTTP⽅法
    def post(self):
        parse = parser.parse_args()
        config_info = parse.get('config_info')
        product_name=config_info['project_name']
        project_no=config_info['project_no']
        version_no=config_info['version_no']
        try:
            deploy_config_table=mydb['deploy_config']
            package_no=product_name+'-'+project_no+'-'+version_no
            config_info['package_no']=package_no
            config_info['update_time']=get_now_time(int(time.time()))
            config_info['status']='生成中'
            query={'package_no':package_no}
            set_data={'$set':config_info}
            is_exist_res=deploy_config_table.find(query)
            if is_exist_res.count()>0:
                deploy_config_table.update_one(query,set_data)
                package_id=is_exist_res['_id']
            else:
                package_id=deploy_config_table.insert_one(config_info).inserted_id
            file_package.soft_package(package_path,images_path,docker_install_path,package_id)
            return [0,'ok']
        except:
            ##deploy_config_table.delete_one({'_id':package_id})
            return [1,traceback.format_exc()]