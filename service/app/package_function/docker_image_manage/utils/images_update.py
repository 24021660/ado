import os,time
from ... import mydb,get_now_time,dockerfile_path,images_path,dockerfile_tar_path,download_url,log_path


def update_image(dockerfile_id):
    docker_manager_table = mydb['docker_image_manage']
    query = {"_id": dockerfile_id}
    res = docker_manager_table.find_one(query)
    shell_res=0
    last_log = 'Successfully tagged'
    if res['create_mode'] == 'org':
        docker_pull_name = res['image_name'] + ':' + res['image_version']
        shell_res = os.system('docker pull ' + docker_pull_name)
    elif res['create_mode'] == 'dockerfile':
        deploy_path = dockerfile_tar_path + str(dockerfile_id) + '.tar.gz'
        os.system('mkdir -p '+dockerfile_path+str(dockerfile_id))
        os.chdir(dockerfile_path)
        shell_res = os.system('tar -zxvf ' + deploy_path+' -C '+str(dockerfile_id))
        os.chdir(dockerfile_path+str(dockerfile_id))
        file_name=os.listdir()[0]
        os.system('mv '+file_name+'/* ./')
        os.system('rm -rf '+file_name)
        if shell_res == 0:
            os.chdir(dockerfile_path + str(dockerfile_id))
            build_res = os.popen('docker build -t ' + res['image_name'] + ':' + res['image_version'] + ' .')
            with open(log_path+str(dockerfile_id)+'.txt','a') as f:
                for build_res_str in build_res:
                    f.write(build_res_str+'\n')
            with open(log_path+str(dockerfile_id)+'.txt','r') as f:
                res_log=f.readlines()
            last_log=res_log[-1]
    if shell_res == 0 and last_log.find('Successfully tagged')!=-1:
        shell_res=os.system(
            'docker save ' + res['image_name'] + ':' + res['image_version'] + ' -o ' + images_path + str(dockerfile_id) +'.tar.gz')
        query = {'_id': dockerfile_id}
        update_str = {'$set': {'update_time': get_now_time(int(time.time())), 'status': '更新完毕',
                               'download': download_url + 'images/' +str(dockerfile_id) + '.tar.gz'}}
        docker_manager_table.update(query, update_str)
    else:
        query = {'_id': dockerfile_id}
        update_str = {'$set': {'update_time': get_now_time(int(time.time())), 'status': '更新失败',
                               'download': download_url + 'images/' + str(dockerfile_id) + '.tar.gz'}}
        docker_manager_table.update(query, update_str)