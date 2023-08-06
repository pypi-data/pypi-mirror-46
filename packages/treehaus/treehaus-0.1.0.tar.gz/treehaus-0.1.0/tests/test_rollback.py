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

class TestRollback(unittest.TestCase):
    

    def test_rollback(self):
        datastore = TestUtils.open()

        index = datastore.getIndex("X")
        index["a"] = 123
        index["b"] = 456
        index["c"] = 789
        datastore.commit()

        index["b"] = 0
        
        datastore.rollback()
        
        self.assertEqual(index["b"],456)

        datastore.close()

        
        
        

if __name__ == '__main__':
    unittest.main()