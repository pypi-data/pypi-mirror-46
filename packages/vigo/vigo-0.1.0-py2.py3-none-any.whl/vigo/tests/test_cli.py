# -*- encoding: utf-8 -*-
import unittest

from vigo.cli import argparser


class TestCLI(unittest.TestCase):
    def test_argparser(self):
        parser = argparser(groups=["foo", "bar"])

        with self.assertRaises(SystemExit):
            parser.parse_args([])

        with self.assertRaises(SystemExit):
            parser.parse_args(["--unknow", "boum"])
