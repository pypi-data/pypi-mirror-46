import os
from functools import wraps

from flask import request, current_app

from hs_rpc import rpc_request_invoke

# 设置grpc调用走python类型
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

def authorization(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 环境变量控制authorize的启动
        start_authorize = current_app.config.get('START_AUTHORIZE')
        if not start_authorize:
            return f(*args, **kwargs)

        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization')
        else:
            raise Exception('用户没有登录!')

        response = rpc_request_invoke('token_verify', message={'token':token}, app='HSRIGHT')
        if response['code'] != 200:
            raise Exception(response['message'])
        return f(*args, **kwargs)
    return decorated_function