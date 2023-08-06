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

def findpos(l,v):
    for i in range(0,len(l)):
        if v < l[i]:
            return i
    return len(l)

class BLeaf(object):

    def __init__(self,tree,parent,keys,values):
        self.tree = tree
        self.parent = parent
        self.keys = keys
        self.values = values

    def setParent(self,parent):
        self.parent = parent

    def next(self):
        return self.parent.getNext(self)

    def prev(self):
        return self.parent.getPrev(self)

    def markModified(self,isModified=True):
        self.tree.setModified(self,isModified)

    def isModified(self):
        return self.tree.isModified(self)

    def getValue(self,key):
        for i in range(0,len(self.keys)):
            if key == self.keys[i]:
                return (self.values[i],True)
        return (None,False)

    def insertValue(self,key,value):
        for i in range(0,len(self.keys)):
            if key == self.keys[i]:
                self.values[i] = value
                return -1
        i = findpos(self.keys,key)
        self.keys.insert(i,key)
        self.values.insert(i,value)
        return i

    def search(self,key):
        (val,found) = self.getValue(key)
        return (self,val,found)

    def insert(self,key,value):
        self.markModified()
        i = self.insertValue(key,value)
        if i == -1:
            return
        if i == 0:
            self.parent.setSplitBoundary(self,key)
        if len(self.keys) > self.tree.nodesize:
            self.split()

    def remove(self,key):
        try:
            i = self.keys.index(key)
        except ValueError as e:
            return False

        self.markModified()

        self.values = self.values[:i]+self.values[i+1:]
        self.keys = self.keys[:i]+self.keys[i+1:]


        if i == 0 and len(self.keys):
            self.parent.setSplitBoundary(self,self.keys[0])

        if len(self.keys) < self.tree.nodesize//2:
            self.parent.merge(self)

        return True


    def split(self):

        newkeys = self.keys[self.tree.nodesize//2:]
        newvalues = self.values[self.tree.nodesize//2:]

        self.keys=self.keys[:self.tree.nodesize//2]
        self.values=self.values[:self.tree.nodesize//2]

        newleaf = self.tree.createLeaf(self.parent,newkeys,newvalues)
        self.parent.insert(newleaf,newkeys[0])


    def max(self):
        return self.keys[len(self.keys)-1]

    def min(self):
        return self.keys[0]

    def count(self):
        return len(self.keys)

    def firstLeaf(self):
        return self

    def lastLeaf(self):
        return self

    def lmove(self,lsib):
        if lsib.count() > self.tree.nodesize/2:
            k = lsib.keys[lsib.count()-1]
            v = lsib.values[lsib.count()-1]
            lsib.remove(k)
            self.insert(k,v)
            return True
        return False

    def rmove(self,rsib):
        if rsib.count() > self.tree.nodesize/2:
            k = rsib.keys[0]
            v = rsib.values[0]
            rsib.remove(k)
            self.insert(k,v)
            return True
        return False

    def lmerge(self,lsib):
        if lsib.count() <= self.tree.nodesize/2:
            lsib.keys = lsib.keys + self.keys
            lsib.values = lsib.values + self.values
            self.parent.removeChild(self)
            self.tree.setRemoved(self)
            lsib.markModified()
            return True
        return False

    def rmerge(self,rsib):
        if rsib.count() <= self.tree.nodesize/2:
            self.keys = self.keys + rsib.keys
            self.values = self.values + rsib.values
            self.parent.removeChild(rsib)
            self.tree.setRemoved(rsib)
            return True
        return False

    def getNext(self,child):
        return self

    def getPrev(self,child):
        return self

    def __call__(self):
        return self


class BNode(object):

    def __init__(self,tree,parent,splits,children):
        self.parent = parent
        self.splits = splits
        self.children = children
        self.tree = tree
        for child in self.children:
            child.setParent(self)

    def setParent(self,parent):
        self.parent = parent

    def __call__(self):
        return self

    def markModified(self,isModified=True):
        self.tree.setModified(self,isModified)

    def isModified(self):
        return self.tree.isModified(self)

    def max(self):
        return self.children[-1]().max()

    def count(self):
        return len(self.children)

    def min(self):
        return self.children[0]().min()

    def search(self,key):
        if len(self.children) == 0:
            return (self,None,False)
        for i in range(0,len(self.children)-1):
            if key < self.splits[i]:
                return self.children[i]().search(key)
        return self.children[len(self.children)-1]().search(key)

    def insert(self,child,minkey):
        self.markModified()

        i = findpos(self.splits,minkey)
        self.children.insert(i+1,child)
        self.splits.insert(i,minkey)

        if len(self.children) > self.tree.nodesize:
            self.split()

    def split(self):
        newsplits = self.splits[self.tree.nodesize//2:]
        newchildren = self.children[self.tree.nodesize//2:]

        split = self.splits[(self.tree.nodesize//2)-1]

        self.children=self.children[:self.tree.nodesize//2]
        self.splits=self.splits[:(self.tree.nodesize//2)-1]

        newnode = self.tree.createNode(self.parent,newsplits,newchildren)

        if not self.parent:
            self.tree.root = self.tree.createNode(None,[split],[self,newnode],False)
        else:
            self.parent.insert(newnode,split)

    def merge(self,child):
        pos = self.childIndex(child)
        if pos > 0 and child().lmove(self.children[pos-1]()):
            return None
        if pos < len(self.children)-1 and child().rmove(self.children[pos+1]()):
            return None
        if pos > 0 and child().lmerge(self.children[pos-1]()):
            return None
        if pos < len(self.children)-1 and child().rmerge(self.children[pos+1]()):
            return None
        if len(self.children) > 1:
            return None

        if len(self.children) == 1 and not self.parent:
            if isinstance(self.children[0](),BNode):
                self.children[0].setParent(None)
                self.tree.root = self.children[0]()

        if len(self.children) == 0:
            self.parent.remove(self)
            self.tree.setRemoved(self)


    def removeChild(self,child):
        self.markModified()
        i = self.childIndex(child)
        self.children = self.children[:i]+self.children[i+1:]
        if i == 0:
            self.parent.setSplitBoundary(self,self.children[0]().min())
            self.splits = self.splits[1:]
        else:
            self.splits = self.splits[:i-1]+self.splits[i:]


        if len(self.children) < self.tree.nodesize/2:
            if self.parent:
                self.parent.merge(self)

    def childIndex(self,child):
        return [c() for c in self.children].index(child)

    def setSplitBoundary(self,child,key):
        i = self.childIndex(child)
        if i == 0:
            if self.parent:
                self.parent.setSplitBoundary(self,key)
        else:
            self.splits[i-1] = key
            self.markModified()

    def firstLeaf(self):
        if len(self.children)>0:
            return self.children[0]().firstLeaf()
        return None

    def lastLeaf(self):
        if len(self.children)>0:
            return self.children[len(self.children)-1]().lastLeaf()
        return None

    def rtraverse(self,kvps):
        if len(self.children)>0:
            self.children[len(self.children)-1]().rtraverse(kvps)

    def lmove(self,lsib):
        if lsib.count() > self.tree.nodesize/2:
            self.children = [lsib.children.pop()]+self.children
            lsib.splits.pop()
            self.splits = [self.children[1]().min()]+self.splits
            self.children[0].setParent(self)
            if self.parent:
                self.parent.setSplitBoundary(self,self.children[0]().min())
            lsib.markModified()
            return True
        return False

    def rmove(self,rsib):
        if rsib.count() > self.tree.nodesize/2:
            rsib.children[0].setParent(self)
            self.children = self.children + rsib.children[:1]
            self.splits = self.splits + [self.children[-1]().min()]
            rsib.splits = rsib.splits[1:]
            rsib.children = rsib.children[1:]
            if self.parent:
                self.parent.setSplitBoundary(rsib,rsib.children[0]().min())
            rsib.markModified()
            return True
        return False

    def lmerge(self,lsib):
        if lsib.count() <= self.tree.nodesize/2:
            lsib.splits = lsib.splits + [self.children[0]().min()] + self.splits
            lsib.children = lsib.children + self.children
            for child in self.children:
                child.setParent(lsib)
            if self.parent:
                self.parent.removeChild(self)
            self.tree.setRemoved(self)
            lsib.markModified()
            return True
        return False

    def rmerge(self,rsib):
        if rsib.count() <= self.tree.nodesize/2:
            self.splits = self.splits + [rsib.children[0]().min()] + rsib.splits
            self.children = self.children + rsib.children
            for child in rsib.children:
                child.setParent(self)
            if self.parent:
                self.parent.removeChild(rsib)
            self.tree.setRemoved(rsib)
            return True
        return False

    def getNext(self,child):
        if child == None:
            return self.children[0]().getNext(None)
        cidx = self.childIndex(child)
        if cidx < len(self.children)-1:
            return self.children[cidx+1]().getNext(None)
        if self.parent:
            return self.parent.getNext(self)
        return None

    def getPrev(self,child):
        if child == None:
            return self.children[len(self.children)-1]().getPrev(None)
        cidx = self.childIndex(child)
        if cidx > 0:
            return self.children[cidx-1]().getPrev(None)
        if self.parent:
            return self.parent.getPrev(self)
        return None

    def next(self):
        if self.parent:
            return self.parent.getNext(self)
        else:
            return None

    def prev(self):
        if self.parent:
            return self.parent.getPrev(self)
        else:
            return None

class Visitor(object):

    def __init__(self,tree,reverse=False,start=None,stop=None,checker=None):
        self.tree = tree
        self.start = start
        self.stop = stop
        self.checker = checker
        if reverse:
            if stop:
                (self.leaf,oldvalue,found) = self.tree.root.search(stop)
                self.index = -1
                for v in self.leaf.keys:
                    if v > stop:
                        break
                    self.index += 1
            else:
                self.leaf = tree.root.lastLeaf()
                self.index = len(self.leaf.keys)-1
        else:
            self.index = 0
            if start:
                (self.leaf,oldvalue,found) = self.tree.root.search(start)
                for v in self.leaf.keys:
                    if v >= start:
                        break
                    self.index += 1
            else:
                self.leaf = tree.root.firstLeaf()
        self.reverse = reverse

    def __next__(self):
        return self.next()

    def next(self):
        if self.checker:
            self.checker()
        if self.reverse:
            while self.index < 0:
                prev = self.leaf.prev()
                if prev:
                    self.leaf = prev
                    self.index = len(self.leaf.keys)-1
                else:
                    raise StopIteration
            val = (self.leaf.keys[self.index],self.tree.decodeValue(self.leaf.values[self.index])[0])
            self.index -= 1
            if self.start and val[0] < self.start:
                raise StopIteration
            return val
        else:
            while self.index >= len(self.leaf.keys):
                self.index = 0
                next = self.leaf.next()
                if next:
                    self.leaf = next
                else:
                    raise StopIteration
            val = (self.leaf.keys[self.index],self.tree.decodeValue(self.leaf.values[self.index])[0])
            self.index += 1
            if self.stop and val[0] > self.stop:
                raise StopIteration
            return val

    def __iter__(self):
        return self


class BTree(object):

    def __init__(self,createEmpty=False,nodesize=10):
        if createEmpty:
            self.root = self.createNode(None,[],[])()
            self.root().children.append(self.createLeaf(self.root,[],[]))

        self.nodesize = nodesize
        self.keycount = 0

    def get(self,key):
        (n,v,found) = self.root.search(key)
        if found:
            return v
        raise KeyError

    def add(self,key,value):
        (n,oldvalue,found) = self.root.search(key)
        if not found or oldvalue != value:
            n.insert(key,value)
        if not found:
            self.keycount += 1

    def createNode(self,parent,splits,children,asReference=True):
        return Node(self,parent,splits,children)

    def createLeaf(self,parent,keys,values):
        return Leaf(self,parent,keys,values)

    def remove(self,key):
        (n,v,found) = self.root.search(key)
        if found:
            n.remove(key)
            self.keycount -= 1
            return v
        else:
            raise KeyError

    def traverse(self,start=None,stop=None,checker=None):
        return Visitor(self,False,start,stop,checker=checker)

    def rtraverse(self,start=None,stop=None,checker=None):
        return Visitor(self,True,start,stop,checker=checker)

    def decodeValue(self,value):
        return (value,0)

    def setModified(self,node_or_leaf,isModified):
        pass

    def isModified(self,node_or_leaf):
        return True

    def setRemoved(self,node_or_leaf):
        pass

    def __delitem__(self,key):
        self.remove(key)

    def __getitem__(self,key):
        return self.get(key)

    def __setitem__(self,key,value):
        self.add(key,value)

    def has_key(self,key):
        try:
            v = self[key]
            return True
        except KeyError:
            return False

    def commit(self):
        return None

    def meta(self):
        return { "key_count":self.keycount }

    def __iter__(self):
        return self.traverse()

    def __len__(self):
        return self.keycount

    def close(self):
        self.commit()

