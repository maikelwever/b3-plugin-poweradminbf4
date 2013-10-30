# -*- encoding: utf-8 -*-

from mock import Mock
from b3.config import CfgConfigParser
from poweradminbf4 import Poweradminbf4Plugin
from tests import Bf4TestCase


class Test_cmd_autoscramble(Bf4TestCase):

    def setUp(self):
        Bf4TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[commands]
autoscramble: mod
""")
        self.p = Poweradminbf4Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.p._scrambler = Mock()
        self.superadmin.connects('superadmin')
        self.superadmin.clearMessageHistory()
        self.p._autoscramble_rounds = None
        self.p._autoscramble_maps = None

    def test_no_arguments(self):
        self.superadmin.says('!autoscramble')
        self.assertEqual(["invalid data. Expecting one of [off, round, map]"], self.superadmin.message_history)
        self.assertIsNone(self.p._autoscramble_rounds)
        self.assertIsNone(self.p._autoscramble_maps)

    def test_bad_arguments(self):
        self.superadmin.says('!autoscramble f00')
        self.assertEqual(["invalid data. Expecting one of [off, round, map]"], self.superadmin.message_history)
        self.assertIsNone(self.p._autoscramble_rounds)
        self.assertIsNone(self.p._autoscramble_maps)

    def test_round(self):
        self.superadmin.says('!autoscramble round')
        self.assertEqual(['Auto scrambler will run at every round start'], self.superadmin.message_history)
        self.assertTrue(self.p._autoscramble_rounds)
        self.assertFalse(self.p._autoscramble_maps)

    def test_r(self):
        self.superadmin.says('!autoscramble r')
        self.assertEqual(['Auto scrambler will run at every round start'], self.superadmin.message_history)
        self.assertTrue(self.p._autoscramble_rounds)
        self.assertFalse(self.p._autoscramble_maps)

    def test_map(self):
        self.superadmin.says('!autoscramble map')
        self.assertEqual(['Auto scrambler will run at every map change'], self.superadmin.message_history)
        self.assertFalse(self.p._autoscramble_rounds)
        self.assertTrue(self.p._autoscramble_maps)

    def test_m(self):
        self.superadmin.says('!autoscramble m')
        self.assertEqual(['Auto scrambler will run at every map change'], self.superadmin.message_history)
        self.assertFalse(self.p._autoscramble_rounds)
        self.assertTrue(self.p._autoscramble_maps)

    def test_off(self):
        self.superadmin.says('!autoscramble off')
        self.assertEqual(['Auto scrambler now disabled'], self.superadmin.message_history)
        self.assertFalse(self.p._autoscramble_rounds)
        self.assertFalse(self.p._autoscramble_maps)
