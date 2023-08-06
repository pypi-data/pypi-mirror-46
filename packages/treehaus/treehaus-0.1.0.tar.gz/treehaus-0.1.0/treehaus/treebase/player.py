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
 
import struct
import time
import pickle

from treehaus.treebase.pbtree import PBTree

class CheckpointNotFoundException(BaseException):

    def __init__(self,checkpointNumber):
        self.checkpointNumber = checkpointNumber

    def __repr__(self):
        return "checkpoint %d not found"%(self.checkpointNumber)

class CheckPointIterator(object):

    def __init__(self,treefile,lastSuperBlockPosition,returnSuperBlocks):
        self.treefile = treefile
        self.lastSuperBlockPosition = lastSuperBlockPosition
        self.returnSuperBlocks = returnSuperBlocks

    def __next__(self):
        return self.next()

    def next(self):
        if self.lastSuperBlockPosition:
            sb = SuperBlock(0,0,0,0,0,"")
            if sb.load(self.treefile,self.lastSuperBlockPosition):
                self.lastSuperBlockPosition = sb.getLastSuperBlockPosition()
                if self.returnSuperBlocks:
                    return sb
                else:
                    return (sb.getUpdateCounter(),sb.getUpdateTime(),sb.getKeyCounts(),sb.getMetadata())
            else:
                print("Broken superblock!")
        raise StopIteration

    def __iter__(self):
        return self

class RootBlock(object):

    ROOTBLOCK_HEADER_MAGIC = bytes("TreeHaus","utf-8")
    
    @staticmethod
    def initialise(treefile,nodesize):
        treefile.seek(0,0)
        magic = treefile.read(8)
        if not magic:
            treefile.write(RootBlock.ROOTBLOCK_HEADER_MAGIC)
            options = { "nodesize": nodesize, "protocol": PLayer.CURRENT_PROTOCOL, "version": PLayer.VERSION }
            pickle.dump(options,treefile)
        else:
            if magic != RootBlock.ROOTBLOCK_HEADER_MAGIC:
                raise Exception("Bad magic")
            options = pickle.load(treefile)
        return options
        
            
class SuperBlock(object):

    # last-superblock-pos update-count update-time index-count index-pos
    SUPERBLOCK_HEADER_MAGIC = bytes("SuperBlock","utf-8")
    SUPERBLOCK_HEADER_FORMAT = "IIIII"
    SUPERBLOCK_HEADER_SIZE = 30 # magic + 5 ints

    def __init__(self,rootNodePositions,lastSuperBlockPosition,updateCounter,keyCounters,updateTime,metadata):
        self.rootNodePositions = rootNodePositions
        self.lastSuperBlockPosition = lastSuperBlockPosition
        self.updateCounter = updateCounter
        self.keyCounters = keyCounters
        self.updateTime = updateTime
        self.metadata = metadata

    def save(self,treefile):
        treefile.seek(0,2)
        pos = treefile.tell()
      
        pickle.dump(self.metadata,treefile)
        pickle.dump(self.rootNodePositions,treefile)
        pickle.dump(self.keyCounters,treefile)
        
        header = SuperBlock.SUPERBLOCK_HEADER_MAGIC+struct.pack(SuperBlock.SUPERBLOCK_HEADER_FORMAT,self.lastSuperBlockPosition,self.updateCounter,self.updateTime,len(self.rootNodePositions),pos)
        pos = treefile.tell()
        treefile.write(header)
        epos = treefile.tell()
        return pos

    def load(self,treefile,pos=None):
        try:
            if pos != None:
                treefile.seek(pos,0)
                pos = treefile.tell()
                line = treefile.read(SuperBlock.SUPERBLOCK_HEADER_SIZE)
            else:
                treefile.seek(0,2)
                treefile.seek(treefile.tell()-SuperBlock.SUPERBLOCK_HEADER_SIZE,0)
                pos = treefile.tell()
                line = treefile.read(SuperBlock.SUPERBLOCK_HEADER_SIZE)
                while pos and line[0:10] != SuperBlock.SUPERBLOCK_HEADER_MAGIC:
                    pos -= 1
                    treefile.seek(pos,0)
                    line = treefile.read(SuperBlock.SUPERBLOCK_HEADER_SIZE)
                if pos == 0:
                    return 0                    
            
            (self.lastSuperBlockPosition,self.updateCounter,self.updateTime,indexCount,indexPos) = struct.unpack(SuperBlock.SUPERBLOCK_HEADER_FORMAT,line[10:])
            self.keyCounters = {}
            self.rootNodePositions = {}
            treefile.seek(indexPos,0)
            self.metadata = pickle.load(treefile)
            self.rootNodePositions = pickle.load(treefile)
            self.keyCounters = pickle.load(treefile)
            return pos
        except OSError as osx:
            return 0
        except Exception as ex:
            raise ex

    def getLastSuperBlockPosition(self):
        return self.lastSuperBlockPosition

    def getRootNodePositions(self):
        return self.rootNodePositions

    def getUpdateCounter(self):
        return self.updateCounter

    def getKeyCounts(self):
        return self.keyCounters

    def getUpdateTime(self):
        return self.updateTime

    def getMetadata(self):
        return self.metadata


class PLayer(object):

    CURRENT_PROTOCOL = 0
    VERSION = "0.1"

    def __init__(self,treefile,checkpointNumber=0,initial_nodesize=10,isReadOnly=False):
        self.treefile = treefile
        self.lastSuperBlockPosition = 0
        self.root = None
        self.updateCounter = 1
        self.isReadOnly = isReadOnly
        self.modified = False

        self.rootNodePositions = {}
        self.keyCounts = {}
        self.ptrees = {}

        self.node_size = RootBlock.initialise(self.treefile,initial_nodesize)["nodesize"]

        sb = SuperBlock({},0,0,{},0,"")
        self.lastSuperBlockPosition = sb.load(treefile)
        if self.lastSuperBlockPosition:
            self.rootNodePositions = sb.getRootNodePositions()
            self.updateCounter = sb.getUpdateCounter()+1
            self.keyCounts = sb.getKeyCounts()

        if checkpointNumber:
            self.updateCounter = 0
    
            for sb in self.checkpoints():
                if checkpointNumber == sb.getUpdateCounter():
                    self.rootNodePositions = sb.getRootNodePositions()
                    self.keyCounts = sb.getKeyCounts()
                    self.isReadOnly = True
                    self.updateCounter = checkpointNumber
                    break
            
            if not self.updateCounter:
                raise CheckpointNotFoundException(checkpointNumber)

        for index in self.rootNodePositions:
            self.ptrees[index] = PBTree(self.treefile,self.rootNodePositions[index],self.node_size,self.isReadOnly,self.updateCounter)
            self.ptrees[index].load()

    def commit(self,metadata):
        updateTime = int(time.time())
        if self.isReadOnly:
            return None
        checkpoint_number = self.updateCounter
        self.save()
        self.modified_nodes = set()
        sb = SuperBlock(self.rootNodePositions,self.lastSuperBlockPosition,self.updateCounter,self.keyCounts,updateTime,metadata)
        self.lastSuperBlockPosition = sb.save(self.treefile)
        self.treefile.flush()
        self.modified = False
        self.updateCounter += 1
        for index in self.ptrees:
            self.ptrees[index].updateUpdateCounter(self.updateCounter)
        self.modified = False
        return checkpoint_number

    def rollback(self):
        sb = SuperBlock({},0,0,{},0,"")
        sb.load(self.treefile,self.lastSuperBlockPosition)
        self.rootNodePositions = sb.getRootNodePositions()
        self.updateCounter = sb.getUpdateCounter()+1
        self.keyCounts = sb.getKeyCounts()
        for index in self.rootNodePositions:
            self.ptrees[index] = PBTree(self.treefile,self.rootNodePositions[index],self.node_size,self.isReadOnly,self.updateCounter)
            self.ptrees[index].load()
        self.modified = False

    def save(self):
        for index in self.ptrees:
            updatedPos = self.ptrees[index].save()
            if updatedPos:
                self.rootNodePositions[index] = updatedPos
        return True

    def load(self):
        for index in self.ptrees:
            self.ptrees[index].load()
            
    def close(self):
        if self.modified:
            self.modified = False
            self.commit("")

    def has_key(self,index,key):
        return self.ptrees[index].has_key(key)

    def get(self,index,key):
        return self.ptrees[index].get(key)

    def remove(self,index,key):
        return self.ptrees[index].remove(key)

    def copy(self,index,from_key,to_key):
        self.ptrees[index].copy(from_key,to_key)

    def openIndex(self,index):
        if index not in self.ptrees:
            self.ptrees[index] = PBTree(self.treefile,0,self.node_size,self.isReadOnly,self.updateCounter)    
        
    def add(self,index,key,value):
        (oldval,updatedCount) = self.ptrees[index].add(key,value)
        self.keyCounts[index] = updatedCount
        self.modified = True
        return oldval

    def clear(self,index):
        self.ptrees[index] = PBTree(self.treefile,0,self.node_size,self.isReadOnly,self.updateCounter)    

    def history(self,index,key,checker=None):
        return self.ptrees[index].history(key,checker=checker)

    def checkpoints(self,returnSuperBlocks=True):
        return CheckPointIterator(self.treefile,self.lastSuperBlockPosition,returnSuperBlocks)

    def getKeyCount(self,index):
        return self.ptrees[index].getKeyCount()

    def traverse(self,index,start=None,stop=None,checker=None):
        return self.ptrees[index].traverse(start,stop,checker=checker)

    def rtraverse(self,index,start=None,stop=None,checker=None):
        return self.ptrees[index].rtraverse(start,stop,checker=checker)

    def listIndices(self):
        l = []
        for key in self.ptrees:
            l.append((key,self.keyCounts.get(key,0)))
        return l

    def removeIndex(self,index):
        del self.ptrees[index]
        del self.rootNodePositions[index]
        del self.keyCounts[index]
        self.modified = True
