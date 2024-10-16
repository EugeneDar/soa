import unittest

from ..app.util.util import parse_http_response
from ..app.main import (
    build_views_and_likes_response,
    build_top_posts_responses,
    build_top_users_responses
)


class TestStatistics(unittest.TestCase):

    def test_http_response_parsing(self):
        self.assertEqual(
            parse_http_response(''),
            []
        )
        self.assertEqual(
            parse_http_response(' 1\t2\na\tb '),
            [
                ['1', '2'],
                ['a', 'b']
            ]
        )

    def test_build_views_and_likes_response(self):
        response = build_views_and_likes_response(
            [
                ['10', '20']
            ]
        )
        self.assertEqual(response.views, 10)
        self.assertEqual(response.likes, 20)

    def test_build_top_posts_response(self):
        responses = build_top_posts_responses(
            [
                ['abc', '1']
            ],
            'likes'
        )
        self.assertEqual(len(responses.posts), 1)
        self.assertEqual(responses.posts[0].post_id, 'abc')
        self.assertEqual(responses.posts[0].views, 0)
        self.assertEqual(responses.posts[0].likes, 1)

        responses = build_top_posts_responses(
            [
                ['abc', '1'],
                ['def', '10'],
                ['ijk', '100'],
            ],
            'views'
        )
        self.assertEqual(len(responses.posts), 3)
        expected_data = [
            ('abc', 1),
            ('def', 10),
            ('ijk', 100),
        ]
        for response, (post_id, views) in zip(responses.posts, expected_data):
            self.assertEqual(response.post_id, post_id)
            self.assertEqual(response.views, views)

    def test_build_top_users_responses(self):
        responses = build_top_users_responses(
            [
                ['abacaba', 100500]
            ]
        )
        self.assertEqual(len(responses.users), 1)
        self.assertEqual(responses.users[0].user_id, 'abacaba')
        self.assertEqual(responses.users[0].likes, 100500)


if __name__ == '__main__':
    unittest.main()
