import unittest

from integration.test_users_service import UserServiceTests
# from post_service_tests import PostServiceTests

test_suite = unittest.TestSuite()

test_suite.addTest(unittest.makeSuite(UserServiceTests))
# test_suite.addTest(unittest.makeSuite(PostServiceTests))

test_runner = unittest.TextTestRunner(verbosity=2)

test_runner.run(test_suite)
