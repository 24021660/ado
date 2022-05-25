from . import api
from flask_restplus import Resource
from .. import mydb
import traceback,json
from bson.json_util import dumps
parser = api.parser()

parser.add_argument('class', type=str, required=False, help='生成方式')
parser.add_argument('image_name', type=str, required=False, help='镜像名称')
parser.add_argument('image_version', type=str, required=False, help='镜像版本')

parser.add_argument('group', type=str, required=False, help='镜像版本',default='false')

@api.route('/images_list')
class BusinessDetails(Resource):
    # 添加接口描述
    @api.doc(description="打包数据打包完成返回0，文件复制未完成返回1")
    @api.expect(parser)
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    # 指定HTTP⽅法
    def get(self):
        try:
            parse = parser.parse_args()
            is_group=parse.get('group')
            print(is_group)
            docker_image_manage_table = mydb['docker_image_manage']
            res=json.loads(dumps(docker_image_manage_table.find()))
            if is_group!='false':
                new_dict = {}
                for i in res:
                    new_dict[i['class']] = []
                for m in res:
                    m['is_checked']=False
                    m['_id']=m['_id']['$oid']
                    new_dict[m['class']].append(m)
                res=new_dict
            return [0,res]
        except:
            return [1, traceback.format_exc()]
