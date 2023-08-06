# -*- coding: utf-8 -*-
from __future__ import print_function

import unittest

from ahds.core import Block


class TestUtils(unittest.TestCase):
    pass


class TestBlock(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.block = Block('block')

    def test_default(self):
        self.assertEqual(self.__class__.block.name, 'block')
        self.assertTrue(hasattr(self.__class__.block, 'name'))
        self.assertTrue(hasattr(self.__class__.block, '__dict__'))
        self.assertTrue(hasattr(self.__class__.block, '__weakref__'))
        self.assertTrue(hasattr(self.__class__.block, '_parent'))

    def test_add_attr(self):
        # non-parent attribute
        self.__class__.block.add_attr('test', 10)
        self.assertTrue(hasattr(self.__class__.block, 'test'))
        self.assertEqual(self.__class__.block.test, 10)
        self.assertEqual(len(self.__class__.block._parent), 0)
        # parent attribute
        self.__class__.block.add_attr('result', 20, isparent=True)
        self.assertEqual(len(self.__class__.block._parent), 1)