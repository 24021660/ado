from . import api
from flask_restplus import Resource
from werkzeug.datastructures import FileStorage
from .. import mydb,dockerfile_tar_path,get_now_time
import traceback,time,requests
from .utils import images_update

parser = api.parser()

parser.add_argument('create_mode', type=str, required=True, help='生成方式')
parser.add_argument('image_name', type=str, required=True, help='镜像名称')
parser.add_argument('image_version', type=str, required=True, help='镜像版本')
parser.add_argument('v', type=str, required=True, help='默认映射目录')
parser.add_argument('port', type=str, required=True, help='默认映射端口')
parser.add_argument('class', type=str, required=True, help='分类方式')
parser.add_argument('file', location='files', type=FileStorage, required=False, help='文件上传')


@api.route('/docker_file_create')
class BusinessDetails(Resource):
    # 添加接口描述
    @api.doc(description="打包数据打包完成返回0，文件复制未完成返回1")
    @api.expect(parser)
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    # 指定HTTP⽅法
    def post(self):
        try:
            parse = parser.parse_args()
            create_mode = parse.get('create_mode')
            image_name = parse.get('image_name')
            image_version = parse.get('image_version')
            v = parse.get('v')
            port = parse.get('port')
            docker_class = parse.get('class')
            docker_image_manage_table = mydb['docker_image_manage']
            query={'create_mode': create_mode, 'image_name': image_name, 'image_version': image_version}
            if docker_image_manage_table.find(query).count()>0:
                return [2,'该镜像已经存在']
            else:

                res = {'create_mode': create_mode, 'image_name': image_name, 'image_version': image_version, 'v': v,
                       'port': port, 'class': docker_class,'status':'生成中','update_time':get_now_time(int(time.time())),'download':'','install_array':'0'}
                images_id=docker_image_manage_table.insert_one(res).inserted_id
                if create_mode == 'dockerfile':
                    docker_file = parse.get('file')
                    docker_file.save(dockerfile_tar_path + str(images_id)+'.tar.gz')
                images_update.update_image(images_id)
                return [0,'ok']
        except:
            docker_image_manage_table.delete_one({'_id':images_id})
            return [1, traceback.format_exc()]
