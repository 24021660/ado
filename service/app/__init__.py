from flask_restplus import Swagger
from flask_restplus import fields
from flask_restplus.model import ModelBase
from flask_restplus.swagger import ref, PY_TYPES
from six import string_types
from inspect import isclass
from flask_restplus import Api
import os,importlib



# 初始化序列化schema，生成swagger
def serialize_schema(self, model):
    if isinstance(model, string_types) and model == 'object':
        return {'type': 'object'}
    if isinstance(model, (list, tuple)):
        model = model[0]
        return {'type': 'array', 'items': self.serialize_schema(model), }
    elif isinstance(model, ModelBase):
        self.register_model(model)
        return ref(model)
    elif isinstance(model, string_types):
        self.register_model(model)
        return ref(model)
    elif isclass(model) and issubclass(model, fields.Raw):
        return self.serialize_schema(model())
    elif isinstance(model, fields.Raw):
        return model.__schema__
    elif isinstance(model, (type, type(None))) and model in PY_TYPES:
        return {'type': PY_TYPES[model]}
    raise ValueError('Model {0} not registered'.format(model))


# 生成swagger
Swagger.serialize_schema = serialize_schema
api = Api(title='Docker Deploy Platform', version='1.0', description='ADo 接口⽂档', doc="/")
# 配置路由
service_dir=[]
service_name = os.listdir('./app')
for service in service_name:
    if service=='ai_service':
        service_dir.append(service)
    if service=='package_function':
        service_dir.append(service)
root_group_config = set()
for ser in service_dir:
    func_dir = os.listdir('./app/' + ser)
    for interface_dir in func_dir:
        if interface_dir[0] != '_':
            interface_name = os.listdir('./app/' + ser + '/' + interface_dir)
            for i in interface_name:
                if i[0:9] == 'interface':
                    import_package = '.' + ser + '.' + interface_dir + '.' + i.split('.')[0]
                    params_ = importlib.import_module(import_package, package='app')
                    api.add_namespace(params_.api)

                    for resource in params_.api.resources:
                        url = resource.urls[0].rstrip('/')
                        root_group_config.add(url)

