#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest

from util.cell import Cell
from util.column_range import ColumnRange


class TestCell(unittest.TestCase):
    def test_from_row_col(self):
        self.assertIsNone(Cell.from_row_col(0, 1))
        self.assertIsNone(Cell.from_row_col(0, 0))
        self.assertIsNone(Cell.from_row_col(1, 0))
        self.assertEqual(Cell.from_row_col(5, 4).get(), (5, 4))

    def test_from_string(self):
        self.assertEqual(Cell.from_string("A1").get(), (1, 1))
        self.assertEqual(Cell.from_string("AA99").get(), (99, 27))
        self.assertIsNone(Cell.from_string("A9A"))
        self.assertIsNone(Cell.from_string("A0"))


class TestColumnRange(unittest.TestCase):
    def test_from_string(self):
        self.assertEqual(ColumnRange.from_string("A-B").start, 1)
        self.assertEqual(ColumnRange.from_string("A-B").end, 2)
        self.assertIsNone(ColumnRange.from_string("A--B"))
        self.assertIsNone(ColumnRange.from_string("AB"))


if __name__ == '__main__':
    unittest.main()
