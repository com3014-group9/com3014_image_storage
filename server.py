from concurrent import futures
import logging
import os
import grpc
from protos import imager_pb2, imager_pb2_grpc
from pymongo import MongoClient
import pprint

def get_filepath(filename, extension):
    return f'images/{filename}{extension}'

class Imager(imager_pb2_grpc.ImagerServicer):
    def __init__(self):
        client = MongoClient("mongodb://localhost:27017")
        self.image_db = client.com3014_images


    def UploadFile(self, request_iterator, context):
        data = bytearray()

        for request in request_iterator:
            if request.metadata.filename and request.metadata.extension:
                filepath = get_filepath(request.metadata.filename, request.metadata.extension)
                continue
            data.extend(request.chunk_data)
        with open(filepath, 'wb') as f:
            print(filepath)

            id = self.image_db.image_data.find_one(sort=[("id", -1)])
            id = id["id"] + 1 if id != None else 0
            self.image_db.image_data.insert_one({"path" : filepath, "id" : id})
            for doc in self.image_db.image_data.find():
                pprint.pprint(doc)

            f.write(data)
            
        return imager_pb2.StringResponse(message='Success!')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    imager_pb2_grpc.add_ImagerServicer_to_server(Imager(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    print("Meow")
    logging.basicConfig()
    serve()