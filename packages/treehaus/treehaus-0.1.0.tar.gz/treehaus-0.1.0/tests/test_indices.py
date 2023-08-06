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

class TestIndices(unittest.TestCase):
    
    def test_indices(self):
        datastore = TestUtils.open()

        indexX = datastore.getIndex("X")
        indexY = datastore.getIndex("Y")
        indexZ = datastore.getIndex("Z")

        indexX["a"] = 123
        indexY["a"] = 456
        indexZ["a"] = 789
        self.assertSetEqual(set(datastore.getIndices()),{("X",1),("Y",1),("Z",1)})
        datastore.close()

        datastore = TestUtils.reopen()
        indexX = datastore.getIndex("X")
        indexY = datastore.getIndex("Y")
        indexZ = datastore.getIndex("Z")

        self.assertEqual(indexX["a"],123)
        self.assertEqual(indexY["a"],456)
        self.assertEqual(indexZ["a"],789)

        datastore.removeIndex("Y")
        self.assertSetEqual(set(datastore.getIndices()),{("X",1),("Z",1)})
        datastore.commit()
        datastore.close()

        datastore = TestUtils.reopen()
        self.assertSetEqual(set(datastore.getIndices()),{("X",1),("Z",1)})
        datastore.close()
        
        

if __name__ == '__main__':
    unittest.main()