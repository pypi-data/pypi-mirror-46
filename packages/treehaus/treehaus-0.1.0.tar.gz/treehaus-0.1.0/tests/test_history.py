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

class TestHistory(unittest.TestCase):
    

    def test_history(self):
        datastore = TestUtils.open()

        index = datastore.getIndex("X")
        index["a"] = 123
        datastore.commit()

        index["a"] = 345
        datastore.commit()

        index["a"] = "def"
        datastore.commit()

        history = [h for h in index.history("a")]
        self.assertEqual([("def",3),(345,2),(123,1)], history)
        datastore.close()

        for (val,checkpoint) in history:
            datastore = TestUtils.reopen(checkpoint=checkpoint)
            index = datastore.getIndex("X")
            self.assertEqual(index["a"],val)
            datastore.close()
        

if __name__ == '__main__':
    unittest.main()