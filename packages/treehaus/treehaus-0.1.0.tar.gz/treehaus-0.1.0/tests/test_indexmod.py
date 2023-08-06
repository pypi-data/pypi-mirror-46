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
import treehaus

import unittest

class TestIndexModifiedException(unittest.TestCase):
    

    def test_index_modified_exception(self):
        with TestUtils.open() as datastore:
            index = datastore.getIndex("X")
            TestUtils.alter(index,{},200,1,0.2)
            index["a"] = 123
            index.copy("a","b")
            index.copy("a","c")
        
        with TestUtils.reopen() as datastore:
            index = datastore.getIndex("X")
            itr = index.traverse()
            kv1 = itr.next()
            index["d"] = 1
            try:
                kv2 = itr.next()
                self.assertTrue(False)
            except treehaus.IndexModifiedException as ex:
                pass
        

if __name__ == '__main__':
    unittest.main()