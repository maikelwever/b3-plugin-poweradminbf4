# -*- encoding: utf-8 -*-

from mock import Mock
from b3.config import CfgConfigParser
from poweradminbf4 import Poweradminbf4Plugin
from tests import Bf4TestCase


class Test_cmd_scramblemode(Bf4TestCase):

    def setUp(self):
        Bf4TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
scramblemode: 20
        """)
        self.p = Poweradminbf4Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.p._scrambler = Mock()
        self.superadmin.connects('superadmin')
        self.superadmin.clearMessageHistory()

    def test_no_arguments(self):
        self.superadmin.says('!scramblemode')
        self.assertEqual(["invalid data. Expecting 'random' or 'score'"], self.superadmin.message_history)
        self.assertFalse(self.p._scrambler.setStrategy.called)

    def test_bad_arguments(self):
        self.superadmin.says('!scramblemode f00')
        self.assertEqual(["invalid data. Expecting 'random' or 'score'"], self.superadmin.message_history)
        self.assertFalse(self.p._scrambler.setStrategy.called)

    def test_random(self):
        self.superadmin.says('!scramblemode random')
        self.assertEqual(['Scrambling strategy is now: random'], self.superadmin.message_history)
        self.p._scrambler.setStrategy.assert_called_once_with("random")

    def test_r(self):
        self.superadmin.says('!scramblemode r')
        self.assertEqual(['Scrambling strategy is now: random'], self.superadmin.message_history)
        self.p._scrambler.setStrategy.assert_called_once_with("random")

    def test_score(self):
        self.superadmin.says('!scramblemode score')
        self.assertEqual(['Scrambling strategy is now: score'], self.superadmin.message_history)
        self.p._scrambler.setStrategy.assert_called_once_with("score")

    def test_s(self):
        self.superadmin.says('!scramblemode s')
        self.assertEqual(['Scrambling strategy is now: score'], self.superadmin.message_history)
        self.p._scrambler.setStrategy.assert_called_once_with("score")
