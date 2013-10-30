# -*- encoding: utf-8 -*-
import time
from mock import patch, call
from mockito import verify, when
from b3.config import CfgConfigParser
from poweradminbf4 import Poweradminbf4Plugin
from tests import Bf4TestCase



class Test_cmd_roundnext(Bf4TestCase):

    @classmethod
    def setUpClass(cls):
        Bf4TestCase.setUpClass()
        cls.sleep_patcher = patch.object(time, "sleep")
        cls.sleep_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.sleep_patcher.stop()

    def setUp(self):
        Bf4TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString("""[commands]
roundnext: 20
        """)
        self.p = Poweradminbf4Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        self.superadmin.connects('superadmin')


    def test_nominal(self):
        when(self.console).write()
        self.superadmin.clearMessageHistory()
        self.superadmin.says('!roundnext')
        self.assertEqual([], self.superadmin.message_history)
        verify(self.console).write(('mapList.runNextRound',))
