import logging
import os
import grpc
from protos import imager_pb2, imager_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = imager_pb2_grpc.ImagerStub(channel)

        response = stub.UploadFile(read_iterfile('test.jpg'))
        print("Imager client received: " + response.message)

def read_iterfile(filepath, chunk_size=1024):
    split_data = os.path.splitext(filepath)
    filename = split_data[0]
    extension = split_data[1]

    metadata = imager_pb2.MetaData(filename=filename, extension=extension)
    yield imager_pb2.UploadFileRequest(metadata=metadata)
    with open(filepath, mode="rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                entry_request = imager_pb2.UploadFileRequest(chunk_data=chunk)
                yield entry_request
            else:  # The chunk was empty, which means we're at the end of the file
                return
        
if __name__ == '__main__':
    logging.basicConfig()
    run()