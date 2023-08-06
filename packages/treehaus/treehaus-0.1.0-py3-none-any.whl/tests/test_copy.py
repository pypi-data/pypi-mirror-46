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

class TestCopy(unittest.TestCase):
    
    def test_copy(self):
        datastore = TestUtils.open()

        index = datastore.getIndex("X")
        TestUtils.alter(index,{},200,1,0.2)
        index["a"] = 123
        index.copy("a","b")
        index.copy("a","c")
        
        datastore.commit()
        
        self.assertEqual(index["a"],123)
        self.assertEqual(index["b"],123)
        self.assertEqual(index["c"],123)

        for key in ["a","b","c"]:
            history = [h for h in index.history(key)]
            self.assertEqual([(123,1)], history)

        bigvalue = "A"*1024*1024
        with TestUtils.open() as datastore:
            big = datastore["big"]
            big["k1"] = bigvalue
            big.copy("k1","k2")
            big.copy("k1","k3")
            big.copy("k1","k3")

    
        fs = TestUtils.getFileSize()
        self.assertTrue(fs > 1024*1024 and fs < 2*1024*1024)
        
        with TestUtils.reopen() as datastore:
            big = datastore["big"]
            self.assertEqual(big["k1"],bigvalue)
            self.assertEqual(big["k2"],bigvalue)
            self.assertEqual(big["k3"],bigvalue)

        datastore.close()
        
if __name__ == '__main__':
    unittest.main()