# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: posts.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bposts.proto\x12\x05posts\"k\n\x04Post\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x0f\n\x07user_id\x18\x04 \x01(\x03\x12\x12\n\ncreated_at\x18\x05 \x01(\x03\x12\x12\n\nupdated_at\x18\x06 \x01(\x03\"D\n\x11\x43reatePostRequest\x12\r\n\x05title\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\x12\x0f\n\x07user_id\x18\x03 \x01(\x03\"P\n\x11UpdatePostRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12\x0f\n\x07user_id\x18\x04 \x01(\x03\"0\n\x11\x44\x65letePostRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\x03\"%\n\x12\x44\x65letePostResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\" \n\x12GetPostByIdRequest\x12\n\n\x02id\x18\x01 \x01(\t\"@\n\x10ListPostsRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x03\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\r\n\x05limit\x18\x03 \x01(\x05\"D\n\x11ListPostsResponse\x12\x1a\n\x05posts\x18\x01 \x03(\x0b\x32\x0b.posts.Post\x12\x13\n\x0btotal_count\x18\x02 \x01(\x03\x32\xbb\x02\n\x0bPostService\x12\x35\n\nCreatePost\x12\x18.posts.CreatePostRequest\x1a\x0b.posts.Post\"\x00\x12\x35\n\nUpdatePost\x12\x18.posts.UpdatePostRequest\x1a\x0b.posts.Post\"\x00\x12\x43\n\nDeletePost\x12\x18.posts.DeletePostRequest\x1a\x19.posts.DeletePostResponse\"\x00\x12\x37\n\x0bGetPostById\x12\x19.posts.GetPostByIdRequest\x1a\x0b.posts.Post\"\x00\x12@\n\tListPosts\x12\x17.posts.ListPostsRequest\x1a\x18.posts.ListPostsResponse\"\x00\x42\x08Z\x06/postsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'posts_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\006/posts'
  _globals['_POST']._serialized_start=22
  _globals['_POST']._serialized_end=129
  _globals['_CREATEPOSTREQUEST']._serialized_start=131
  _globals['_CREATEPOSTREQUEST']._serialized_end=199
  _globals['_UPDATEPOSTREQUEST']._serialized_start=201
  _globals['_UPDATEPOSTREQUEST']._serialized_end=281
  _globals['_DELETEPOSTREQUEST']._serialized_start=283
  _globals['_DELETEPOSTREQUEST']._serialized_end=331
  _globals['_DELETEPOSTRESPONSE']._serialized_start=333
  _globals['_DELETEPOSTRESPONSE']._serialized_end=370
  _globals['_GETPOSTBYIDREQUEST']._serialized_start=372
  _globals['_GETPOSTBYIDREQUEST']._serialized_end=404
  _globals['_LISTPOSTSREQUEST']._serialized_start=406
  _globals['_LISTPOSTSREQUEST']._serialized_end=470
  _globals['_LISTPOSTSRESPONSE']._serialized_start=472
  _globals['_LISTPOSTSRESPONSE']._serialized_end=540
  _globals['_POSTSERVICE']._serialized_start=543
  _globals['_POSTSERVICE']._serialized_end=858
# @@protoc_insertion_point(module_scope)
