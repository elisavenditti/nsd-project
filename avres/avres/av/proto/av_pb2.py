# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/av.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eproto/av.proto\x12\x05proto\"(\n\x05input\x12\x0c\n\x04\x66ile\x18\x01 \x01(\x0c\x12\x11\n\tnum_chunk\x18\x02 \x01(\x05\"-\n\x06output\x12\x10\n\x08response\x18\x01 \x01(\t\x12\x11\n\tnum_chunk\x18\x02 \x01(\x05\x32;\n\nSendBinary\x12-\n\nsendBinary\x12\x0c.proto.input\x1a\r.proto.output(\x01\x30\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.av_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _INPUT._serialized_start=25
  _INPUT._serialized_end=65
  _OUTPUT._serialized_start=67
  _OUTPUT._serialized_end=112
  _SENDBINARY._serialized_start=114
  _SENDBINARY._serialized_end=173
# @@protoc_insertion_point(module_scope)
