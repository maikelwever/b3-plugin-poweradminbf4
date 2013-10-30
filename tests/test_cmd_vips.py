# -*- encoding: utf-8 -*-
from mock import call, Mock
from mockito import when
from b3.config import CfgConfigParser
from poweradminbf4 import Poweradminbf4Plugin
from tests import Bf4TestCase


class Test_cmd_vips(Bf4TestCase):
    def setUp(self):
        Bf4TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""
[commands]
vips: mod
""")
        self.p = Poweradminbf4Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

        self.console.say = Mock()
        self.console.saybig = Mock()

        self.moderator.connects("moderator")

        self.joe.connects('joe')
        self.joe.teamId = 2


    def test_empty_vip_list(self):
        when(self.console).write(('reservedSlotsList.list', 0)).thenReturn([])
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vips")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('No VIP connected', self.moderator.message_history[0])


    def test_4_vips(self):
        when(self.console).write(('reservedSlotsList.list', 0)).thenReturn(['name1', 'name2', 'name3', 'name2'])
        when(self.console).write(('reservedSlotsList.list', 4)).thenReturn(['name4'])
        when(self.console).write(('reservedSlotsList.list', 5)).thenReturn([])
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vips")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('No VIP connected', self.moderator.message_history[0])


    def test_4_vips_one_is_connected(self):
        when(self.console).write(('reservedSlotsList.list', 0)).thenReturn(['name1', 'name2', 'name3', 'Joe'])
        when(self.console).write(('reservedSlotsList.list', 4)).thenReturn([])
        self.joe.connects("Joe")
        self.moderator.connects("moderator")
        self.moderator.message_history = []
        self.moderator.says("!vips")
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('Connected VIPs: Joe', self.moderator.message_history[0])

