# Copyright 2017 TreeHaus Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
 
from tests.test_utils import TestUtils
import unittest
from time import sleep

class TestCheckpoints(unittest.TestCase):
    

    def test_checkpoints(self):
        with TestUtils.open() as datastore:

            index = datastore.getIndex("X")
            for idx in range(100):
                index[idx] = idx
            datastore.commit("A")
            sleep(2)

            for idx in range(100,200):
                index[idx] = idx
            datastore.commit("B")
            sleep(2)

            for idx in range(200,300):
                index[idx] = idx
            datastore.commit("C")
            sleep(2)

            updates = list(datastore.getUpdates())
            self.checkUpdates(updates)

        with TestUtils.reopen() as datastore:
            updates = list(datastore.getUpdates())
            self.checkUpdates(updates)

    def checkUpdates(self,updates):
        # check timestamps 
        for idx in range(1,len(updates)):
            self.assertGreater(updates[idx-1][1],updates[idx][1]) 
        updates_without_timestamp = list(map(lambda x:(x[0],x[2],x[3]),updates))
        
        expected = [(3,{"X":300},"C"),(2,{"X":200},"B"),(1,{"X":100},"A")]
        self.assertEqual(updates_without_timestamp,expected)
   

if __name__ == '__main__':
    unittest.main()