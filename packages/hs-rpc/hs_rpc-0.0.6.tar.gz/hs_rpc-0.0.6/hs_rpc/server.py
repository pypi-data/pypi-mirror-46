import grpc
import time
from concurrent import futures

from hs_rpc.proto import rpc_data_pb2_grpc
from hs_rpc.proto.rpc_data_pb2 import Reply
from hs_rpc.proto.rpc_data_pb2_grpc import add_GreeterServicer_to_server
from hs_rpc.rpc import rpc_server_invoke

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(rpc_data_pb2_grpc.GreeterServicer):

    def handle_request(self, request, context):
        response = rpc_server_invoke(request.message)
        return Reply(message=response)


def serve(app):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_GreeterServicer_to_server(Greeter(), server)

    server.add_insecure_port('[::]:{}'.format(app.config['RPC_PORT'] or 8120))
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

