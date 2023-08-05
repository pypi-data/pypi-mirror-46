# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import pickle

class Node(object):
    """Syntax node Python library for programming languages

"""

    def __new__(cls, node, uppernode, **kwargs):

        obj = super(Node, cls).__new__(cls)

        obj.nodename = cls.__name__
        obj.uppernode = uppernode
        obj.subnodes = []
        obj.nodetypes = []

        constructor = getattr(obj, "construct", None)

        if constructor is None:
            raise Exception("'construct' bound method is not found.")

        elif callable(constructor):
            constructor(node) 

        else:
            raise Exception("'construct' attribute is not callable.")

        return obj

    def add_nodetype(self, nodetype):
        self.nodetypes.append(nodetype)

    def add_subnode(self, node):
        subnode = Node(node, self)
        self.subnodes.append(subnode)
        return subnode

    def write(self, output):

        with open(output, "wb") as f:
            pickle.dump(self, f)
