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

class TestDelete(unittest.TestCase):
    
    def test_delete(self):
        datastore = TestUtils.open()

        index = datastore.getIndex("X")
        TestUtils.alter(index,{},200,1,0.2)
        index["a"] = 123
        index["b"] = 456
        index["c"] = 789
        
        del index["b"]
        datastore.commit()
        
        self.assertFalse("b" in index)

        datastore.close()
        
        

if __name__ == '__main__':
    unittest.main()