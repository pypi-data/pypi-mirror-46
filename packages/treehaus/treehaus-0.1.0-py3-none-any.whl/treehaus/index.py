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

class ReadOnlyException(BaseException):

    def __init__(self):
        pass

    def __repr__(self):
        return "TreeHaus datastore is opened in read-only mode"

class StoreClosedException(BaseException):

    def __init__(self):
        pass

    def __repr__(self):
        return "TreeHaus datastore has been closed"

class IndexModifiedException(BaseException):

    def __init__(self):
        pass

    def __repr__(self):
        return "TreeHaus index has been modified"

class Checker(object):

    def __init__(self,index):
        self.index = index
        self.index_modified = False
        
    def markIndexModified(self):
        self.index_modified = True

    def __call__(self):
        if self.index.datastore.isClosed():
            raise StoreClosedException

        if self.index_modified:
            raise IndexModifiedException

class Index(object):

    def __init__(self,player,index,datastore,readOnly):
        self.player = player
        self.index = index
        self.datastore = datastore
        self.readOnly = readOnly
        self.player.openIndex(self.index)
        self.checkers = []

    def check(self,requiresWrite=False):
        if self.datastore.isClosed():
            raise StoreClosedException
        if self.readOnly and requiresWrite:
            raise ReadOnlyException
        if requiresWrite:
            # invalidate any opened iterators
            for checker in self.checkers:
                checker.markIndexModified()
            self.checkers = []

    def __delitem__(self,key):
        """
        Delete an item from this index

        Arguments:
             key: the key value to delete

        Returns:
             the value of the key that was removed

        Raises:
             treehaus.StoreClosedException: raised if the store has been closed
             treehaus.ReadOnlyException: (if the store is opened read-only)
             KeyError: (if the key does not exist in the index)

        A way you might use me is:

        >>> from treehaus import TreeHaus
        >>> th = TreeHaus.open("data.th")
        >>> books = th.getIndex("books")
        >>> removed_book = del books["0140449132"]

        """
        self.check(True)
        self.player.remove(self.index,key)

    def __getitem__(self,key):
        """
        Get an item from this index

        Arguments:
             key: the key value to retrieve

        Returns:
             the value of the key

        Raises:
             KeyError: (if the key does not exist in the index)

        A way you might use me is:

        >>> from treehaus import TreeHaus
        >>> th = TreeHaus.open("data.th")
        >>> books = th.getIndex("books")
        >>> book_details = books["0140449132"]

        """
        self.check()
        return self.player.get(self.index,key)

    def __setitem__(self,key,value):
        """
        Add or modify an item in this index

        Arguments:
             key: the key value to add
             value: the associated value to add

        Raises:
             treehaus.StoreClosedException: raised if the store has been closed
             treehaus.ReadOnlyException: (if the store is opened read-only)
             
        A way you might use me is:

        >>> from treehaus import TreeHaus
        >>> th = TreeHaus.open("data.th")
        >>> books = th.getIndex("books")
        >>> books["0140449132"] = { "title": "Crime and Punishment", "author":"Fyodor Mikhailovich Dostoyevsky" }

        """
        self.check(True)
        self.player.add(self.index,key,value)

    def put(self,key,value):
        """
        Add or modify an item in this index

        Arguments:
             key: the key value to add
             value: the associated value to add

        Returns:
             if the key already existed in the index its value is returned, otherwise None is returned

        Raises:
            treehaus.StoreClosedException: raised if the store has been closed
            treehaus.ReadOnlyException: (if the store is opened read-only)
             
        A way you might use me is:

        >>> from treehaus import TreeHaus
        >>> th = TreeHaus.open("data.th")
        >>> books = th.getIndex("books")
        >>> books.put("0140449132", { "title": "Crime and Punishment", "author":"Fyodor Mikhailovich Dostoyevsky" })

        """
        self.check(True)
        self.player.add(self.index,key,value)

    def pop(self,key,defaultvalue=None):
        """
        Remove and return a value for a specified key

        Arguments:
             key: the key to retrieve and remove
             defaultvalue: the value to return if the key was not found

        Returns:
             if the key already existed in the index its value is returned, otherwise defaultvalue is returned

        Raises:
             treehaus.StoreClosedException: raised if the store has been closed
             treehaus.ReadOnlyException: (if the store is opened read-only)
             
        A way you might use me is:

        >>> from treehaus import TreeHaus
        >>> th = TreeHaus.open("data.th")
        >>> books = th.getIndex("books")
        >>> removed_book = books.pop("0140449132")

        """
        self.check(True)
        v = self.player.remove(self.index,v)
        if v == None:
            v = defaultvalue
        if v == None:
            raise KeyError(key)
        return v      

    def clear(self):
        """
        Remove all keys from the index

        Raises:
             treehaus.ReadOnlyException: (if the store is opened read-only)
             treehaus.StoreClosedException: raised if the store has been closed

        A way you might use me is:

        >>> from treehaus import TreeHaus
        >>> th = TreeHaus.open("data.th")
        >>> books = th.getIndex("books")
        >>> books.clear()
        >>> len(books)
        0

        """
        self.check(True)
        self.player.clear(self.index)

    def get(self,key,defaultvalue=None):
        """
        Get an item from this index

        Arguments:
            key: the key value to retrieve
            defaultvalue: a value to return if the key was not found

        Returns:
            the value of the key if found in the index, or the defaultvalue otherwise

        Raises:
            treehaus.StoreClosedException: raised if the store has been closed
        
        A way you might use me is:

        >>> from treehaus import TreeHaus
        >>> th = TreeHaus.open("data.th")
        >>> books = th.getIndex("books")
        >>> book_details = books.get("0140449132",{"title":"unknown","author":"unknown"})

        """
        self.check()
        try:
            return self[key]
        except KeyError:
            return defaultvalue

    def __contains__(self,key):
        """
        Test if a key exists in the index

        Arguments:
            key: the key value to test
            
        Returns:
            True if the key is found in the index, or False otherwise

        Raises:
            treehaus.StoreClosedException: raised if the store has been closed

        A way you might use me is:

        >>> from treehaus import TreeHaus
        >>> th = TreeHaus.open("data.th")
        >>> books = th.getIndex("books")
        >>> "0140449132" in books
        True

        """
        self.check()
        return self.player.has_key(self.index,key)
    
    def traverse(self,start=None,stop=None):
        """
        Iterate over the index in key order

        Keyword Arguments:
            start: start the iterator from this key value
            stop: end the iterator at this key value

        Returns:
            an iterator which returns (key,value) pairs

        Raises:
            treehaus.StoreClosedException: raised if the store has been closed
            treehaus.IndexModifiedException: raised during iteration if the index was modified after the iterator was opened

        A way you might use me is:

        >>> from treehaus import TreeHaus
        >>> th = TreeHaus.open("data.th")
        >>> books = th.getIndex("books")
        >>> for (isbn,details) in books:
        >>>     print(str(isbn))
        
        """
        self.check()
        checker = Checker(self)
        self.checkers.append(checker)
        return self.player.traverse(self.index,start,stop,checker=checker)

    def rtraverse(self,start=None,stop=None):
        """
        Iterate over the index in reverse order

        Keyword Arguments:
            start: start the iterator from this key value
            stop: end the iterator at this key value

        Returns:
            an iterator which returns (key,value) pairs in reverse key order

        Raises:
            treehaus.StoreClosedException: raised if the store has been closed
            treehaus.IndexModifiedException: raised during iteration if the index was modified after the iterator was opened

        A way you might use me is:

        >>> from treehaus import TreeHaus
        >>> th = TreeHaus.open("data.th")
        >>> books = th.getIndex("books")
        >>> for (isbn,details) in books.rtraverse():
        >>>     print(str(isbn))
        
        """
        self.check()
        checker = Checker(self)
        self.checkers.append(checker)
        return self.player.rtraverse(self.index,start,stop,checker=checker)

    def history(self,key):
        """
        Return a history of the values assigned to a key, most recently assigned value first

        Arguments:
            key: the key of interest
            
        Returns:
            an iterator which returns (updateNumber,value) pairs indicating that the key was assigned that value at that updateNumber

        Raises:
            treehaus.StoreClosedException: raised if the store has been closed
            treehaus.IndexModifiedException: raised during iteration if the index was modified after the iterator was opened

        A way you might use me is:

        >>> from treehaus import TreeHaus
        >>> th = TreeHaus.open("data.th")
        >>> books = th.getIndex("books")
        >>> for (updateNumber,value) in books.history("0140449132"):
        >>>     print(str((updateNumber,value)))
        (45,{ "title": "Crime and Punishment", "author":"Fyodor Mikhailovich Dostoyevsky" })
        (23,{ "title": "Crimes and Punishment", "author":"Dave Dostoyevsky" })
        
        """
        self.check()
        checker = Checker(self)
        self.checkers.append(checker)
        return self.player.history(self.index,key,checker=checker)

    def update(self,other):
        """
        Update the index with multiple (key,value) pairs 

        Arguments:
            other: dict or iterable returning (key,value) pairs
            
        Raises:
            treehaus.StoreClosedException: raised if the store has been closed

        A way you might use me is:

        >>> from treehaus import TreeHaus
        >>> th = TreeHaus.open("data.th")
        >>> books = th.getIndex("books")
        >>> newtitles = {}
        >>> newtitles["9780140449136"] = { "title": "Crime and Punishment", "author":"Fyodor Mikhailovich Dostoyevsky" }
        >>> newtitles["9781853260629"] = { "title":"War and Peace", "author":"Leo Tolstoy" }
        >>> books.update(newtitles)
        >>> books["9781853260629"]
        { "title":"War and Peace", "author":"Leo Tolstoy" }
        >>> books["9780140449136"]
        { "title": "Crime and Punishment", "author":"Fyodor Mikhailovich Dostoyevsky" }
        >>> th.commit()
        54

        """
        self.check()
        for (k,v) in other:
            self[k] = v

    def __iter__(self):
        return self.player.traverse(self.index)

    def __len__(self):
        """
        Get the index length

        Returns:
            the number of keys in the index

        Raises:
            treehaus.StoreClosedException: raised if the store has been closed

        A way you might use me is:

        >>> from treehaus import TreeHaus
        >>> th = TreeHaus.open("data.th")
        >>> books = th.getIndex("books")
        >>> len(books)
        146

        """
        self.check()    
        return self.player.getKeyCount(self.index)


    def copy(self,from_key,to_key):
        """
        Copy a value from one key to another, but without creating a copy of the value in the file.

        Arguments:
            from_key: the key to copy
            to_key: the key to create or modify

        Raises:
            treehaus.StoreClosedException: raised if the store has been closed
            treehaus.ReadOnlyException: (if the store is opened read-only)
            KeyError: if from_key is not found in the index             
        
        A way you might use me is:

        >>> from treehaus import TreeHaus
        >>> th = TreeHaus.open("data.th")
        >>> books = th.getIndex("books")
        >>> books.copy("0140449132", "9780140449136")

        """
        self.check(True)
        self.player.copy(self.index,from_key,to_key)

        

