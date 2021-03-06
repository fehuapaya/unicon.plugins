"""
Unittests for fxos/ftd plugin

Uses the unicon.mock.mock_device script to test the plugin.

"""

__author__ = "dwapstra"


import unittest

from unicon import Connection
from unicon.eal.dialogs import Dialog
from unicon.plugins.generic.statements import GenericStatements

generic_statements = GenericStatements()
password_stmt = generic_statements.password_stmt
escape_char_stmt = generic_statements.escape_char_stmt


class TestFxosFtdPlugin(unittest.TestCase):

    def test_connect(self):
        c = Connection(hostname='Firepower',
                       start=['mock_device_cli --os fxos --state fxos_connect'],
                       os='fxos',
                       series='ftd',
                       username='cisco',
                       tacacs_password='cisco')
        c.connect()
        self.assertEqual(c.spawn.match.match_output, '\r\nFirepower# ')
        return c

    def test_execute_scope(self):
        c = self.test_connect()
        c.switchto('chassis scope /system/services')
        r = c.execute(['create ntp-server 192.168.200.101', 'commit-buffer'])
        self.assertEqual(r, {'commit-buffer': '', 'create ntp-server 192.168.200.101': ''})
        self.assertEqual(c.spawn.match.match_output, 'commit-buffer\r\nFirepower /system/services # ')

    def test_execute_scope2(self):
        c = self.test_connect()
        c.execute(['scope service-profile'], allow_state_change=True)

    def test_console_execute(self):
        c = Connection(hostname='Firepower',
                       start=['mock_device_cli --os fxos --state chassis_exec'],
                       os='fxos',
                       series='ftd',
                       username='cisco',
                       tacacs_password='cisco',
                       enable_password='cisco',
                       line_password='cisco')
        c.connect()
        c.switchto('ftd expert')
        c.execute(['sudo su -'],
                  reply=Dialog([password_stmt, escape_char_stmt]),
                  allow_state_change=True)

    def test_switchto_states(self):
        states = [
            'chassis',
            'chassis scope /system',
            'fxos',
            'local-mgmt',
            'cimc',
            'cimc 1',
            'module console',
            'module 1 console',
            'ftd console',
            'ftd expert',
            'ftd expert root'
            ]
        c = Connection(hostname='Firepower',
                       start=['mock_device_cli --os fxos --state fxos_exec'],
                       os='fxos',
                       series='ftd',
                       username='cisco',
                       tacacs_password='cisco',
                       enable_password='cisco',
                       line_password='cisco')
        c.connect()
        for state in states:
            c.switchto(state)


if __name__ == "__main__":
    unittest.main()
