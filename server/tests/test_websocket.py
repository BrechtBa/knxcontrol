#!/usr/bin/env python3
################################################################################
#    Copyright 2016 Brecht Baeten
#    This file is part of HomeCon.
#
#    HomeCon is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    HomeCon is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with HomeCon.  If not, see <http://www.gnu.org/licenses/>.
################################################################################

import unittest
import time
import json

from common import HomeConTestCase, Client


class WebsocketTests(HomeConTestCase):

    def test_send_message(self):
        
        hc = self.start_homecon()
        client = Client('ws://127.0.0.1:9024')

        client.send({'somekey':'somevalue'})
        client.send({'event':'state_set','path':'somepath','value':1})

        client.close()

        self.stop_homecon(hc)
        self.save_homecon_log()


        # check for success in the log
        with open(self.logfile) as f:
            success = False
            for l in f:
                if 'sent {\'somekey\': \'somevalue\'}' in l:
                    success = True

            self.assertEqual(success,True)



if __name__ == '__main__':
    # run tests
    unittest.main()
