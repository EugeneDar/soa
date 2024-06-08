import unittest
from unittest.mock import MagicMock

from ..app.util.util import get_field, proto_post_to_dict
from ..app.api.posts.posts_pb2 import Post


class TestUsers(unittest.TestCase):

    def test_get_field(self):
        request = MagicMock()
        request.json = {'field1': 'value1', 'field2': 'value2'}

        self.assertEqual(get_field(request, 'field1'), 'value1')
        self.assertEqual(get_field(request, 'field3', 'default_value'), 'default_value')

    def test_proto_post_to_dict(self):
        proto_post = Post(id='ABC', title='Test Title', content='Test Content', user_id=101, created_at=2024, updated_at=2025)
        expected_dict = {
            'id': 'ABC',
            'title': 'Test Title',
            'content': 'Test Content',
            'user_id': 101,
            'created_at': 2024,
            'updated_at': 2025
        }

        self.assertEqual(proto_post_to_dict(proto_post), expected_dict)


if __name__ == '__main__':
    unittest.main()
