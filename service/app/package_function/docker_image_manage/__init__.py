"""
部署文件安装
"""

from flask_restplus import Namespace

api = Namespace("docker_image_manage", path="/docker_image_manage", description="镜像同步")
