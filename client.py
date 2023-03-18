import logging
import os
import grpc
from protos import hello_pb2, hello_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(hello_pb2.HelloRequest(name='John Doe', age=30))
        print("Greeter client received: " + response.message)
        
if __name__ == '__main__':
    logging.basicConfig()
    run()