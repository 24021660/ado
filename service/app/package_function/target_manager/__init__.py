"""
部署文件安装
"""

from flask_restplus import Namespace

api = Namespace("target_manager", path="/target_manager", description="配置文件读取")
