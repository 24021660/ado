"""
部署文件安装
"""

from flask_restplus import Namespace

api = Namespace("package_config", path="/package_config", description="配置文件读取")
