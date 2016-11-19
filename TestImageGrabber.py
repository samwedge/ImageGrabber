import unittest
import os
from ImageGrabber import *


class MyTestCase(unittest.TestCase):

    def test_create_directory(self):
        dirname = 'aL6D45kaH2F1jUU1eMDf'
        self.assertFalse(os.path.exists(dirname))
        create_directory(dirname)
        self.assertTrue(os.path.exists(dirname))
        os.removedirs(dirname)
        self.assertFalse(os.path.exists(dirname))


if __name__ == '__main__':
    unittest.main()
