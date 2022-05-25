from . import api
from flask_restplus import Resource
from .. import mydb
parser=api.parser()

parser.add_argument('test', type=str, required=True, help='软件打包序列号')


@api.route('/test')
class BusinessDetails(Resource):
    # 添加接口描述
    @api.doc(description="打包数据打包完成返回0，文件复制未完成返回1")
    @api.expect(parser)
    # 指定请求返回值
    @api.response(200, description="success", model='object')
    # 指定HTTP⽅法
    def get(self):
        parse = parser.parse_args()
        test_name = parse.get('test')
        if test_name=='project_deploy':
            head_transfer={}
            res=[]
            table_header_table=mydb['table_header']
            header_info=table_header_table.find_one({'table_name':test_name})
            title_list=header_info['table_header']
            data = [{'package_no':'aiops-001-1_0','project_name': 'aiops', 'project_no': '001', 'version_no': '1.0',
                    'update_time': '2021-10-1 10:59:00', 'status': '1','download_url':'www.baidu.com'},{'package_no':'aiops-001-2_0','project_name': 'aiops', 'project_no': '001', 'version_no': '2.0',
                    'update_time': '2021-10-1 10:49:00', 'status': '0','download_url':'www.baidu.com'},{'package_no':'aiops-001-3_0','project_name': 'aiops', 'project_no': '001', 'version_no': '3.0',
                    'update_time': '2021-10-1 10:49:00', 'status': '0','download_url':'www.baidu.com'}]

            for title_info in title_list:
                head_transfer[title_info['header']]=title_info['org']

            for i in data:
                res_data={}
                print(i['status'])
                res_data['package_no']=i['package_no']
                if i['status'] == '1':
                    i['status'] = '更新完成'
                    download = '下载'
                    download_url=i['download_url']

                else:
                    i['status'] = '更新中..'
                    download_url='#'
                    download = '等待'
                print(download)
                print(i['status'])
                for transfer_key in head_transfer:
                    res_data[transfer_key] = i[head_transfer[transfer_key]]
                res_data['下载']=download
                res_data['download_url']=download_url

                res.append(res_data)
        return res


