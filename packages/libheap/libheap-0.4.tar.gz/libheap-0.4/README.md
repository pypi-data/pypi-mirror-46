# libheap
here is an implementation of a general min/max heap library, including heap and indexHeap, which not only supports the usual <em>insert</em> , <em>delete-the-minimum/maximum</em>, <em>peeking at the minimum/maximum</em> operations, but also <em>deletion, heapification, key query</em> and <em>key changing</em> operations.  
Indexheap is a significant heap structure which stores and sorts (index,key) pairs according to their key, it is essential in efficient implementation of Dijkstra's algorithm, Prim's algorithm and other variants.  
Meanwhile, it also includes class UF which supports quick union and quick find.  
## Acknowledgement
this library is coded by reference to [algs4](https://algs4.cs.princeton.edu/code/). Much appreciation!

## Usage

```python
class Heap:
    #Initializes an empty priority queue or with existent keys.
    #keys: a list of existent keys
    #min: a boolean variable denoting whether it is min heap or not
    #compare: DIY compare function of keys, format: def compare(x,y)
    def __init__(self, keys: list = None, min=True, compare=None):

    def insert(self, key):

    def pop(self):

    def top(self):

    def empty(self):

    def size(self):

    def delete(self, key):

    def __contains__(self, item):

class IndexHeap:
    def __init__(self, indices: list = None, keys: list = None, min=True, compare=None):

    def empty(self):

    def size(self):

    def pop(self):

    def top(self):

    def insert(self, index, key):

    def changeKey(self, index, key):

    def keyOf(self, index):

    def delete(self, index):
    
    def __contains__(self, item):

```

documentation to be completed    
## Installation
method 1: pip install --user libheap  
method 2: download this project, and run "python setup.py install"  
only support python3