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

from treehaus import TreeHaus
import unittest
import os
import os.path
import random
from os.path import join, exists
import tempfile


class TestUtils(object):

    PATH = join(tempfile.gettempdir(),"treehaus.th") 

    @staticmethod
    def getFileSize():
        with open(TestUtils.PATH,"r") as f:
            f.seek(0,2)
            return f.tell()

    @staticmethod
    def open():
        if exists(TestUtils.PATH):
            os.unlink(TestUtils.PATH) 
        TreeHaus.create(TestUtils.PATH)     
        return TreeHaus.open(TestUtils.PATH) 

    @staticmethod
    def reopen(checkpoint=None,readOnly=False):
        return TreeHaus.open(TestUtils.PATH,openAtUpdate=checkpoint,readOnly=readOnly) 

    @staticmethod
    def alter(index,test,num,dthresh,dprob):

        for i in range(0,num):
            changed = False
            if i > dthresh:
                if random.random() < dprob:
                    oldkeys = list(test.keys())
                    if len(oldkeys)>0:
                        rmkey = oldkeys[int(random.random()*len(oldkeys))]
                        del index[rmkey]
                        if test != None:
                            del test[rmkey]
                        changed = True
            if not changed:
                k = TestUtils.make_key(8)
                v = TestUtils.make_key(25)
                # v = TestUtils.make_value()

                index[k] = v
                if test != None:
                    test[k] = v

    @staticmethod
    def check(index,test):
        # assert len(index) == len(test)
        for k in test.keys():
            if index[k] != test[k]:
                print("checktree error:" + k + "/" + str(index[k]) + "/" + str(test[k]))
                assert False

        for kv in index:
            k = kv[0]
            v = kv[1]
            if v != None:

                if test[k] != v:
                    print("checktree error:" + k + "/" + str(v) + "/" + str(test[k]))
                    assert False

        for idx in range(0,20):
            k = TestUtils.make_key(8)
            if k not in test and k in index:
                assert False

    @staticmethod
    def traverse_check(index,test,lwb=None,upb=None,reverse=False):
        subset = {}
        if reverse:
            i = index.rtraverse(lwb,upb)
        else:
            i = index.traverse(lwb,upb)
        lastk = None
        for kv in i:
            k = kv[0]
            v = kv[1]
            assert k
            subset[k] = v
            if lastk:
                if reverse:
                    assert k < lastk
                else:
                    assert k > lastk
            lastk = k

        for k in test.keys():
            if (lwb and k < lwb) or (upb and k > upb):
                assert k not in subset
            else:
                assert k in subset

    @staticmethod
    def make_key(num_chars,choices=['a','b','c','d','e','f']):
        key = ''
        for c in range(0,num_chars):
            key += choices[int(random.random()*len(choices))]
        return key

    @staticmethod
    def make_value():
        p = random.random()
        if p < 0.2:
            return 500*p
        if p < 0.4:
            return int(500*p)
        if p < 0.6:
            return TestUtils.make_key(5)
        return { "k1": TestUtils.make_key(5) }

    @staticmethod
    def make_key_pair(num_chars):
        k1 = TestUtils.make_key(num_chars)
        k2 = TestUtils.make_key(num_chars)
        if k1 < k2:
            return (k1,k2)
        else:
            return (k2,k1)