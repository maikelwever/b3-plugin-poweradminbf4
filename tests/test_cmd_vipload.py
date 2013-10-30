# -*- encoding: utf-8 -*-
from mockito import when
from b3.config import CfgConfigParser
from b3.parsers.frostbite2.protocol import CommandFailedError
from poweradminbf4 import Poweradminbf4Plugin
from tests import Bf4TestCase, logging_disabled


class Test_cmd_vipload(Bf4TestCase):
    def setUp(self):
        Bf4TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
vipload: 20
        """)
        with logging_disabled():
            self.p = Poweradminbf4Plugin(self.console, self.conf)
            self.p.onLoadConfig()
            self.p.onStartup()
            self.moderator.connects("moderator")

    def test_nominal(self):
        when(self.console).write(('reservedSlotsList.list', 0)).thenReturn([])
        when(self.console).write(('reservedSlotsList.load',)).thenReturn([])
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vipload")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('VIP list loaded from disk (0 name loaded)', self.moderator.message_history[0])

    def test_nominal_2(self):
        when(self.console).write(('reservedSlotsList.list', 0)).thenReturn(['foo', 'bar'])
        when(self.console).write(('reservedSlotsList.list', 2)).thenReturn([])
        when(self.console).write(('reservedSlotsList.load',)).thenReturn([])
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vipload")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('VIP list loaded from disk (2 names loaded)', self.moderator.message_history[0])

    def test_frostbite_error(self):
        when(self.console).write(('reservedSlotsList.load',)).thenRaise(CommandFailedError(['f00']))
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vipload")
        self.assertEqual(["Error: f00"], self.moderator.message_history)