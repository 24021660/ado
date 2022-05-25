"""
部署文件安装
"""

from flask_restplus import Namespace

api = Namespace("soft_package", path="/soft_package", description="文件部署")
