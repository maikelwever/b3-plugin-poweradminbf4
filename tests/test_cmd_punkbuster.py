# -*- encoding: utf-8 -*-
import time
from mock import patch, call
from mockito import when, verify
from b3.config import CfgConfigParser
from poweradminbf4 import Poweradminbf4Plugin
from tests import Bf4TestCase



class Test_cmd_punkbuster(Bf4TestCase):

    def setUp(self):
        Bf4TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
punkbuster-punk: 20
        """)
        self.p = Poweradminbf4Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.superadmin.connects('superadmin')


    def test_pb_inactive(self):
        when(self.console).write(('punkBuster.isActive',)).thenReturn(['false'])
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!punkbuster test')
        self.assertEqual(['Punkbuster is not active'], self.superadmin.message_history)

    def test_pb_active(self):
        when(self.console).write(('punkBuster.isActive',)).thenReturn(['true'])
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!punkbuster test')
        self.assertEqual([], self.superadmin.message_history)
        verify(self.console).write(('punkBuster.pb_sv_command', 'test'))

    def test_pb_active(self):
        when(self.console).write(('punkBuster.isActive',)).thenReturn(['true'])
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!punk test')
        self.assertEqual([], self.superadmin.message_history)
        verify(self.console).write(('punkBuster.pb_sv_command', 'test'))
