"""
部署文件安装
"""

from flask_restplus import Namespace

api = Namespace("base_function", path="/", description="测试接口")
