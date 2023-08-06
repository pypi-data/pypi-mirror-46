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

import unittest
import random
import os
import os.path
from time import sleep
from os.path import exists
import gc
import copy

from tests.test_utils import TestUtils
from treehaus import TreeHaus

class TestWorkload(unittest.TestCase):

    def test_workload(self):

        self.store = TestUtils.open()
        self.index = self.store.getIndex("index1")
        self.test = {} # mirror the index contents in a dict

        num_versions = 20
        num_traverses = 0
        checkpoints = []
        
        random.seed(21)

        for v in range(0,num_versions):
            
            TestUtils.alter(self.index,self.test,200,1,0.2)
            checkpoint_number = self.store.commit()
            if checkpoint_number:
                checkpoints.append((checkpoint_number,copy.deepcopy(self.test)))
                TestUtils.check(self.index,self.test)
            
        TestUtils.traverse_check(self.index,self.test,None,None,False)

        TestUtils.traverse_check(self.index,self.test,None,None,True)

        for i in range(0,num_traverses):
            (lwb,upb) = test_utils.make_key_pair(5)
            TestUtils.traverse_check(self.index,self.test,lwb,upb,True)
            TestUtils.traverse_check(self.index,self.test,lwb,None,True)
            TestUtils.traverse_check(self.index,self.test,lwb,upb,False)
            TestUtils.traverse_check(self.index,self.test,None,upb,True)
            TestUtils.traverse_check(self.index,self.test,None,upb,False)
   
        for (checkpoint_number, test_dict) in checkpoints:
            with TreeHaus.open(TestUtils.PATH,openAtUpdate=checkpoint_number) as cp: 
                cp_index = cp.getIndex("index1")
                TestUtils.check(cp_index,test_dict)

if __name__ == '__main__':
    unittest.main()