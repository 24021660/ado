"""
部署文件安装
"""

from flask_restplus import Namespace

api = Namespace("computer_manager", path="/computer_manager", description="测试接口")
