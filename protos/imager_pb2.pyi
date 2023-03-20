from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MetaData(_message.Message):
    __slots__ = ["extension", "filename"]
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    extension: str
    filename: str
    def __init__(self, filename: _Optional[str] = ..., extension: _Optional[str] = ...) -> None: ...

class StringResponse(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class UploadFileRequest(_message.Message):
    __slots__ = ["chunk_data", "metadata"]
    CHUNK_DATA_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    chunk_data: bytes
    metadata: MetaData
    def __init__(self, metadata: _Optional[_Union[MetaData, _Mapping]] = ..., chunk_data: _Optional[bytes] = ...) -> None: ...
