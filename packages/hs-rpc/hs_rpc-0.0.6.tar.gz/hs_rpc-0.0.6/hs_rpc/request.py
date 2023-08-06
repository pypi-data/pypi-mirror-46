'''
编译命令
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./rpc_data.proto
'''
import json
import os

import grpc
from flask import current_app

from hs_rpc.exceptions import MissingConfigError
from hs_rpc.proto.rpc_data_pb2 import Request
from hs_rpc.proto.rpc_data_pb2_grpc import GreeterStub

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"


def rpc_request_invoke(func, message, app):
    '''
    调用指定app的rpc服务方的一个函数
    :param func: 服务方的函数名
    :param message: 服务方函数需要的参数，字典类型，如果服务方需要token验证message必须携带token
    :param app: 将要调用哪个app的rpc服务
    :return:
    '''
    app_rpc = current_app.config.get((app + '_' + 'rpc').upper())
    if app_rpc is None:
        raise MissingConfigError('未配置 %s 的服务地址' % app)
    if not isinstance(message, dict):
        raise MissingConfigError('message类型必须为字典类型')

    message.update({'func': func})
    channel = grpc.insecure_channel(app_rpc)
    stub = GreeterStub(channel)
    response = stub.handle_request(Request(message=json.dumps(message, ensure_ascii=True)))
    return json.loads(response.message)
