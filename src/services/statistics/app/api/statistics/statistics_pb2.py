# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: statistics.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10statistics.proto\x12\nstatistics\"\'\n\x14ViewsAndLikesRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\t\"5\n\x15ViewsAndLikesResponse\x12\r\n\x05views\x18\x01 \x01(\x03\x12\r\n\x05likes\x18\x02 \x01(\x03\"f\n\x0fTopPostsRequest\x12\x33\n\x07sort_by\x18\x01 \x01(\x0e\x32\".statistics.TopPostsRequest.SortBy\"\x1e\n\x06SortBy\x12\t\n\x05LIKES\x10\x00\x12\t\n\x05VIEWS\x10\x01\"H\n\x04Post\x12\x0f\n\x07post_id\x18\x01 \x01(\t\x12\x11\n\tauthor_id\x18\x02 \x01(\t\x12\r\n\x05views\x18\x03 \x01(\x03\x12\r\n\x05likes\x18\x04 \x01(\x03\"3\n\x10TopPostsResponse\x12\x1f\n\x05posts\x18\x01 \x03(\x0b\x32\x10.statistics.Post\"5\n\x04User\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\r\n\x05views\x18\x02 \x01(\x03\x12\r\n\x05likes\x18\x03 \x01(\x03\"3\n\x10TopUsersResponse\x12\x1f\n\x05users\x18\x01 \x03(\x0b\x32\x10.statistics.User\"\x07\n\x05\x45mpty2\xfb\x01\n\x11StatisticsService\x12\\\n\x15GetTotalViewsAndLikes\x12 .statistics.ViewsAndLikesRequest\x1a!.statistics.ViewsAndLikesResponse\x12H\n\x0bGetTopPosts\x12\x1b.statistics.TopPostsRequest\x1a\x1c.statistics.TopPostsResponse\x12>\n\x0bGetTopUsers\x12\x11.statistics.Empty\x1a\x1c.statistics.TopUsersResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'statistics_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_VIEWSANDLIKESREQUEST']._serialized_start=32
  _globals['_VIEWSANDLIKESREQUEST']._serialized_end=71
  _globals['_VIEWSANDLIKESRESPONSE']._serialized_start=73
  _globals['_VIEWSANDLIKESRESPONSE']._serialized_end=126
  _globals['_TOPPOSTSREQUEST']._serialized_start=128
  _globals['_TOPPOSTSREQUEST']._serialized_end=230
  _globals['_TOPPOSTSREQUEST_SORTBY']._serialized_start=200
  _globals['_TOPPOSTSREQUEST_SORTBY']._serialized_end=230
  _globals['_POST']._serialized_start=232
  _globals['_POST']._serialized_end=304
  _globals['_TOPPOSTSRESPONSE']._serialized_start=306
  _globals['_TOPPOSTSRESPONSE']._serialized_end=357
  _globals['_USER']._serialized_start=359
  _globals['_USER']._serialized_end=412
  _globals['_TOPUSERSRESPONSE']._serialized_start=414
  _globals['_TOPUSERSRESPONSE']._serialized_end=465
  _globals['_EMPTY']._serialized_start=467
  _globals['_EMPTY']._serialized_end=474
  _globals['_STATISTICSSERVICE']._serialized_start=477
  _globals['_STATISTICSSERVICE']._serialized_end=728
# @@protoc_insertion_point(module_scope)