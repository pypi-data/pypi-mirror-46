import abc
import collections
import functools
import math

from .. import base


def entropy(counts):
    """Computes entropy using counts.

    Parameters:
        counts (collections.Counter)

    References:

        1. `Calculating entropy <https://www.johndcook.com/blog/2013/08/17/calculating-entropy/>`_

    """
    N = sum(counts.values())
    return math.log2(N) - sum(n * math.log2(n) for n in counts.values()) / N


class Node(abc.ABC):

    @abc.abstractmethod
    def get_leaf(self, x):
        """Recursively search for the leaf that contains ``x``."""


class Branch(Node):

    def __init__(self, splitter, left, right):
        self.splitter = splitter
        self.left = left
        self.right = right

    def get_leaf(self, x):
        if self.splitter(x):
            return self.left.next()
        return self.right.next()


class Leaf(Node):

    def __init__(self):
        self.class_counts = collections.Counter()
        dd = collections.defaultdict
        self.feature_counts = dd(functools.partial(dd, collections.Counter))

    def get_leaf(self, x):
        return self

    @property
    def is_pure(self):
        return len(self.class_counts) <= 1


class DecisionTreeClassifier(base.MultiClassifier):

    def __init__(self):
        self.root = Leaf()

    def fit_one(self, x, y):

        # Assign the observation to a leaf
        leaf = self.root.get_leaf(x)

        # Update the leaf's overall class counts
        leaf.class_counts.update((y,))

        # Update the leaf's class counts per feature value
        for i, xi in x.items():
            leaf.feature_counts[i][xi].update((y,))

        if not leaf.is_pure:

            leaf_entropy = entropy(leaf.class_counts)

            for i in leaf.feature_counts:
                pass
