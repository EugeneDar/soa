import sys
import os
import unittest


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from app.util.util import parse_http_response
from app.main import (
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
        self.assertEquals(response.views, 10)
        self.assertEquals(response.likes, 20)

    def test_build_top_posts_response(self):
        responses = build_top_posts_responses(
            [
                ['abc', '1']
            ],
            'likes'
        )
        self.assertEquals(len(responses), 1)
        self.assertEquals(responses[0].post_id, 'abc')
        self.assertEquals(responses[0].views, 0)
        self.assertEquals(responses[0].likes, 1)

        responses = build_top_posts_responses(
            [
                ['abc', '1'],
                ['def', '10'],
                ['ijk', '100'],
            ],
            'views'
        )
        self.assertEquals(len(responses), 3)
        expected_data = [
            ('abc', 1),
            ('def', 10),
            ('ijk', 100),
        ]
        for response, (post_id, views) in zip(responses, expected_data):
            self.assertEquals(response.post_id, post_id)
            self.assertEquals(response.views, views)

    def test_build_top_users_responses(self):
        responses = build_top_posts_responses(
            [
                ['abacaba', 100500]
            ]
        )
        self.assertEquals(len(responses), 1)
        self.assertEquals(responses[0].user_id, 'abacaba')
        self.assertEquals(responses[0].likes, 100500)



if __name__ == '__main__':
    unittest.main()
