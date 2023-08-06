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

from treehaus.treebase.btree import BLeaf, BNode, BTree

import random
import weakref
import struct
import pickle

class HistoryIterator(object):

    def __init__(self,tree,key,checker=None):
        self.tree = tree
        self.key = key
        self.checker = checker
        try:
            (self.value,self.prevpos,self.updatedAt) = self.tree.getWithPrevPos(key)
        except KeyError:
            self.value = None
            self.prevpos = 0
            self.updatedAt = 0

    def __next__(self):
        return self.next()

    def next(self):
        if self.checker:
            self.checker()
        nextval = self.value
        updatedAt = self.updatedAt
        if nextval == None:
            raise StopIteration
        if self.prevpos:
            (self.value,self.prevpos,self.updatedAt) = self.tree.decodeValue(self.prevpos)
        else:
            self.value = None
        return (nextval,updatedAt)

    def __iter__(self):
        return self

class ChildRef(object):

    def __init__(self,tree,parent,pos,child):
        self.tree = tree
        self.parent = parent
        self.pos = pos
        if child:
            self.tree.touchNodeOrLeaf(child)
            fn = lambda x: tree.unloadNodeOrLeaf(child)
            self.child = weakref.ref(child,fn)
        else:
            self.child = None

    def __call__(self):
        if self.child:
            child = self.child()
            if child:
                self.tree.touchNodeOrLeaf(child)
                return child

        c = self.tree.loadNodeOrLeaf(self.parent,self.pos)
        self.tree.touchNodeOrLeaf(c)
        tree = self.parent.tree
        isleaf = isinstance(c,PLeaf)
        fn = lambda x: tree.unloadNodeOrLeaf(isleaf)
        self.child = weakref.ref(c,fn)
        child = self.child()
        if not child:
            print("NULL child, pos="+str(self.pos))
        return self.child()

    def getPos(self):
        return self.pos

    def save(self,treefile):
        pos = 0
        if self.child:
            child = self.child()
            if child:
                pos = child.save(treefile)
                if pos:
                    self.pos = pos
        return pos

    def setParent(self,parent):
        self.parent = parent
        if self.child:
            child = self.child()
            if child:
                child.parent = parent

class PLeaf(BLeaf):

    def __init__(self,tree,parent,keys,values):
        BLeaf.__init__(self,tree,parent,keys,values)
        self.pos = None
        
    def save(self,treefile):
        modified = self.isModified()

        if modified:
            self.start = self.tree.updateCounter
            treefile.seek(0,2)
            self.pos = treefile.tell()
            pickle.dump(("L",self.keys,self.values),treefile)
            self.markModified(False)
            return self.pos
        return 0
        
    def setValue(self,key,value):
        return Leaf.setValue(key,value)


class PNode(BNode):

    def __init__(self,tree,parent,splits,children):
        BNode.__init__(self,tree,parent,splits,children)
        self.pos = None
        
    def save(self,treefile):
        c = len(self.children)-1
        while c >= 0:
            if self.children[c].save(treefile):
                self.markModified()
            c -= 1
        modified = self.isModified()

        if modified:
            self.start = self.tree.updateCounter
            children = list(map(lambda c:c.getPos(),self.children))
            treefile.seek(0,2)
            self.pos = treefile.tell()
            pickle.dump(("N",self.splits,children),treefile)
            self.markModified(False)
            return self.pos
        else:
            return 0

        
class ValueBlock(object):

    @staticmethod
    def writeValue(treefile,lastPos,updateCounter,value,ref_pos=0):
        if ref_pos:
            treefile.seek(ref_pos,0)
            (_,_,_,ref_ref_pos) = pickle.load(treefile)
            if ref_ref_pos:
                ref_pos = ref_ref_pos
        treefile.seek(0,2)
        pos = treefile.tell()
        pickle.dump((value,lastPos,updateCounter,ref_pos),treefile)
        return pos

    @staticmethod
    def readValue(treefile,pos):
        treefile.seek(pos,0)
        (value,lastPos,updateCounter,ref_pos) = pickle.load(treefile)
        if ref_pos:
            treefile.seek(ref_pos,0)
            (value,_,_,_) = pickle.load(treefile)
        return (value,lastPos,updateCounter)

class PBTree(BTree):
    
    def __init__(self,treefile,rootNodePosition,node_size,isReadOnly,updateCounter):
        self.node_size = node_size
        self.rootNodePosition = rootNodePosition
        self.modified_nodes = set()
        self.cache = {}
        self.cache_size = 10
        self.root = None
        self.isReadOnly = isReadOnly
        self.treefile = treefile
        self.updateCounter = updateCounter
        self.keyCount = 0
        BTree.__init__(self,self.rootNodePosition==0,self.node_size)

    def updateUpdateCounter(self,updatedUpdateCounter):
        self.updateCounter = updatedUpdateCounter
        
    def createNode(self,parent,splits,children,asReference=True):
        for idx in range(0,len(children)):
            if not isinstance(children[idx],ChildRef):
                children[idx] = ChildRef(self,parent,0,children[idx])
        node = PNode(self,parent,splits,children)
        node.markModified()
        if asReference:
            return ChildRef(self,parent,0,node)
        else:
            return node

    def createLeaf(self,parent,keys,values):
        leaf = PLeaf(self,parent,keys,values)
        leaf.markModified()
        return ChildRef(self,parent,0,leaf)

    def loadNodeOrLeaf(self,parent,pos):
        self.treefile.seek(pos,0)
        (ctype,a1,a2) = pickle.load(self.treefile)
        if ctype == 'N':
            node = PNode(self,parent,a1,[])
            children = list(map(lambda x:ChildRef(self,node,x,None),a2))
            node.children = children
            return node
        else:
            return PLeaf(self,parent,a1,a2)
            
    def unloadNodeOrLeaf(self,isleaf):
        pass

    def load(self):
        self.root = self.loadNodeOrLeaf(None,self.rootNodePosition)

    def save(self):
        return self.root.save(self.treefile)

    def has_key(self,key):
        s = self.root().search(key)
        return s[1] != None

    def get(self,key):
        (val,oldpos,updatedAt) = self.readValue(BTree.get(self,key))
        return val

    def getWithPrevPos(self,key):
        return self.decodeValue(BTree.get(self,key))
        
    def remove(self,key):
        oldvalue = BTree.remove(self,key)
        if oldvalue != None:
            self.modified = True
            self.keyCount -= 1
        return oldvalue
        
    def add(self,key,value):
        s = self.root().search(key)
        n = s[0]
        oldpos = s[1]
        oldval = None
        if oldpos:
            oldval = self.decodeValue(oldpos)[0]

        if not oldpos or oldval != value:
            if not oldpos:
                oldpos = 0
            n.insert(key,self.writeValue(value,oldpos))
            self.modified = True
            if not oldpos:
                self.keyCount += 1
        return (oldval,self.keyCount)

    def copy(self,from_key,to_key):
        f = self.root().search(from_key)
        t = self.root().search(to_key)
        from_pos = f[1]
        last_pos = t[1]
        n = t[0]
        if not from_pos:
            raise KeyError(from_key)

        n.insert(to_key,self.writeValueRef(from_pos,last_pos))
        self.modified = True
        if not last_pos:
            self.keyCount += 1

    def history(self,key,checker=None):
        return HistoryIterator(self,key,checker=checker)

    def setModified(self,node_or_leaf,isModified):
        if isModified:
            self.modified_nodes.add(node_or_leaf)
        else:
            try:
                self.modified_nodes.remove(node_or_leaf)
            except:
                print("missing remove")
                pass

    def setRemoved(self,node_or_leaf):
        self.setModified(node_or_leaf,True)

    def isModified(self,node_or_leaf):
        return node_or_leaf in self.modified_nodes

    def touchNodeOrLeaf(self,node_or_leaf):
        if node_or_leaf in self.cache:
            return
        while len(self.cache) > self.cache_size:
            self.cache.popitem()
        self.cache[node_or_leaf] = 1

    def writeValue(self,value,lastPos):
        return ValueBlock.writeValue(self.treefile,lastPos,self.updateCounter,value)

    def writeValueRef(self,pos,lastPos):
        return ValueBlock.writeValue(self.treefile,lastPos,self.updateCounter,None,pos)

    def readValue(self,pos):
        return ValueBlock.readValue(self.treefile,pos)

    def decodeValue(self,pos):
        return self.readValue(pos)

    def tell(self):
        return self.treefile.tell()

    def flush(self):
        self.treefile.flush()

    def getKeyCount(self):
        return self.keyCount

    def traverse(self,start=None,stop=None,checker=None):
        return super(PBTree,self).traverse(start,stop,checker=checker)

    def rtraverse(self,start=None,stop=None,checker=None):
        return super(PBTree,self).rtraverse(start,stop,checker=checker)



