# -*- encoding: utf-8 -*-

from mock import Mock
from b3.config import CfgConfigParser
from poweradminbf4 import Poweradminbf4Plugin
from tests import Bf4TestCase


class Test_cmd_scramble(Bf4TestCase):

    def setUp(self):
        Bf4TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
scramble: 20
        """)
        self.p = Poweradminbf4Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.p._scrambler = Mock()
        self.superadmin.connects('superadmin')
        self.superadmin.clearMessageHistory()

    def test_none(self):
        self.p._scrambling_planned = None
        self.superadmin.says('!scramble')
        self.assertEqual(['Teams will be scrambled at next round start'], self.superadmin.message_history)
        self.assertTrue(self.p._scrambling_planned)

    def test_true(self):
        self.p._scrambling_planned = True
        self.superadmin.says('!scramble')
        self.assertEqual(['Teams scrambling canceled for next round'], self.superadmin.message_history)
        self.assertFalse(self.p._scrambling_planned)

    def test_false(self):
        self.p._scrambling_planned = False
        self.superadmin.says('!scramble')
        self.assertEqual(['Teams will be scrambled at next round start'], self.superadmin.message_history)
        self.assertTrue(self.p._scrambling_planned)