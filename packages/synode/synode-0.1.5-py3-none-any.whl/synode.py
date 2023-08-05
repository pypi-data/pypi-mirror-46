# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import sys
import abc
import pickle

if sys.version_info >= (3, 0):
    Object = abc.ABCMeta("Object", (object,), {})

else:
    Object = abc.ABCMeta("Object".encode("utf-8"), (object,), {})

class Node(Object):
    """Syntax node Python library for programming languages

"""

    def __new__(cls, node, uppernode, **kwargs):

        obj = super(Node, cls).__new__(cls)

        obj.nodename = cls.__name__
        obj.uppernode = uppernode
        obj.subnodes = []
        obj.nodetypes = []

        cls.construct(obj, node)

        return obj

    @abc.abstractmethod
    def construct(self, node):
        pass

    def add_nodetype(self, nodetype):
        self.nodetypes.append(nodetype)

    def add_subnode(self, node):
        subnode = Node(node, self)
        self.subnodes.append(subnode)
        return subnode

    def write(self, output):

        with open(output, "wb") as f:
            pickle.dump(self, f)
