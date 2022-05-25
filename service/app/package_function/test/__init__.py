"""
部署文件安装
"""

from flask_restplus import Namespace

api = Namespace("test", path="/test", description="测试接口")
