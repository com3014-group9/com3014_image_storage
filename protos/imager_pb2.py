# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/imager.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13protos/imager.proto\"!\n\x0eStringResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"/\n\x08MetaData\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x11\n\textension\x18\x02 \x01(\t\"S\n\x11UploadFileRequest\x12\x1d\n\x08metadata\x18\x01 \x01(\x0b\x32\t.MetaDataH\x00\x12\x14\n\nchunk_data\x18\x02 \x01(\x0cH\x00\x42\t\n\x07request2?\n\x06Imager\x12\x35\n\nUploadFile\x12\x12.UploadFileRequest\x1a\x0f.StringResponse\"\x00(\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.imager_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _STRINGRESPONSE._serialized_start=23
  _STRINGRESPONSE._serialized_end=56
  _METADATA._serialized_start=58
  _METADATA._serialized_end=105
  _UPLOADFILEREQUEST._serialized_start=107
  _UPLOADFILEREQUEST._serialized_end=190
  _IMAGER._serialized_start=192
  _IMAGER._serialized_end=255
# @@protoc_insertion_point(module_scope)