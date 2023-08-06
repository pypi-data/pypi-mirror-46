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

from treehaus.treebase.player import PLayer, CheckpointNotFoundException
from treehaus.index import Index, StoreClosedException

from os.path import exists

class UpdateNotFoundException(BaseException):

    def __init__(self,updateNumber):
        self.updateNumber = updateNumber

    def __repr__(self):
        return "update %d was not found in store"%(self.updateNumber)

class TreeHaus(object):

    @staticmethod
    def create(path,initial_nodesize=10):
        """
        Create an empty TreeHaus store

        Arguments:
            path(str): the path of the file to create, which should not already exist

        Keyword Arguments:
            initial_nodesize(int): integer >= 2, define the size of btree internal nodes

        Raises:
            FileExistsError: raised if the file already exists
        
        A way you might use me is

        >>> path = "data.th"
        >>> TreeHaus.create(path)
        
        """
        if exists(path):
            raise FileExistsError(path)

        treefile = open(path,"w+b")
        player = PLayer(treefile,None,initial_nodesize,False)
        player.close()
        treefile.close()

    @staticmethod
    def open(path,readOnly=False,openAtUpdate=None):
        """
        Open a TreeHaus store

        Arguments:
            path(str): the path of the file to open, which point to a created TreeHaus file

        Keyword Arguments:
            readOnly(bool): whether file should be opened in read-only mode (True) or writable mode (False)
            openAtUpdate(int): open the file in read-only mode at particular update number

        Returns:
            a :class:`treehaus.TreeHaus` instance allowing the data in the file to be accessed

        Raises:
            FileNotExistsError: raised if the file does not exists
            
        A way you might use me is

        >>> path = "data.th"
        >>> th = TreeHaus.open(path)

        """
        if not exists(path):
            raise FileNotFoundError(path)
        if readOnly:
            treefile = open(path,"r+b")
        else:
            treefile = open(path,"a+b")
        try:
            return TreeHaus(treefile,openAtUpdate,readOnly)
        except CheckpointNotFoundException:
            raise UpdateNotFoundException(openAtUpdate)

    @staticmethod
    def getVersion():
        """
        Get the TreeHaus version

        Returns:
            Version number of TreeHaus as a string in the format "VMajor.VMinor"
            
        A way you might use me is:

        >>> TreeHaus.version()
        "0.1"

        """
        return PLayer.VERSION

    def __init__(self,treefile,checkpoint,readOnly):
        self.readOnly = readOnly
        self.treefile = treefile    
        self.player = PLayer(self.treefile,checkpoint,0,readOnly)
        self.closed = False

    def getIndex(self,indexName):
        """
        Obtain an index within the store, creating if it does not already exist

        Arguments:
            indexName(str): the name of the index to obtain

        Returns:
            a :class:`treehaus.Index` instance allowing key-value pairs to be written and read

        Raises:
            treehaus.StoreClosedException: raised if the store has been closed
        
        A way you might use me is:

        >>> path = "data.th"
        >>> th = TreeHaus.open(path)
        >>> books = th.getIndex("books")

        """
        self.check()
        return Index(self.player,indexName,self,self.readOnly)

    def __getitem__(self,indexName):
        return self.getIndex(indexName)

    def getIndices(self):
        """
        Get the names and numbers of stored keys of all indices in the store

        Returns:
            a list of strings containing the names of all indices
        
        Raises:
            treehaus.StoreClosedException: raised if the store has been closed
        
        A way you might use me is:

        >>> path = "~/data.th"
        >>> th = TreeHaus.open(path)
        >>> th.getIndices()
        [('books', 107),('records', 33)]
        """
        self.check()
        return self.player.listIndices()

    def getUpdates(self):
        """
        Get an iterator over the set of updates that were successfully committed to the store

        Returns:
            iterator returning (updateNumber,timestamp,indexNameCardinalityMap,metadata) tuples

        Raises:
            treehaus.StoreClosedException: raised if the store has been closed
        
        Most recent updates are returned first
        
        A way you might use me is:

        >>> path = "~/data.th"
        >>> th = TreeHaus.open(path)
        >>> th.getUpdates().next()
        (23, 1558273679, {'books': 107, 'records': 33}, 'add latest titles')
        
        """
        self.check()
        return self.player.checkpoints(False)

    def removeIndex(self,indexName):
        """
        Remove an index from the store

        Arguments:
            indexName(str): the name of the index to remove

        Raises:
            treehaus.StoreClosedException: raised if the store has been closed
        
        A way you might use me is:

        >>> path = "~/data.th"
        >>> th = TreeHaus.open(path)
        >>> th.removeIndex("records")

        """
        self.check()
        self.player.removeIndex(indexName)

    def commit(self,metadata=""):
        """
        Commit all outstanding changes in the store to file

        Returns:
            an updateNumber for the commit.  

        Raises:
            treehaus.StoreClosedException: raised if the store has been closed
        
        A way you might use me is:

        >>> path = "~/data.th"
        >>> th = TreeHaus.open(path)
        >>> th.getIndex("books")["9781853260629"]={"title":"War and Peace","author":"Leo Tolstoy"}
        >>> th.commit()
        24

        """
        self.check()
        return self.player.commit(metadata)

    def rollback(self):
        """
        Cancel all outstanding changes made to the store

        Raises:
            treehaus.StoreClosedException: raised if the store has been closed
        
        A way you might use me is:

        >>> path = "~/data.th"
        >>> th = TreeHaus.open(path)
        >>> th.getIndex("books")["9781853260629"]={"title":"War and Peace","author":"David Tolstoy"}
        >>> th.rollback() # mistake - should be Leo not David - do not persist this change

        """
        self.check()
        self.player.rollback()

    def close(self):
        """
        close the instance if it is not already closed, any in-progress updates will be committed

        after close is called any opened indices or iterators can no longer be used

        A way you might use me is:

        >>> path = "~/data.th"
        >>> with TreeHaus.open(path) as th:
        >>>     ... read and write to indexes
        >>> ... after with block ends, TreeHaus.close() will be called

        """
        if not self.closed:
            self.player.close()
            self.treefile.close()
            self.treefile = None
            self.closed = True

    def isClosed(self):
        return self.closed

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def check(self):
        if self.closed:
            raise StoreClosedException