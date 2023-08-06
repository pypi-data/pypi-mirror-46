# encoding: utf-8

import copy


class Combination(object):


    def __init__(self, values):
        self.values = values


    def rank_of(self, v):
        return self.values.index(v)


    def value_of(self, r):
        return self.values[r]


    def copy(self):

        values = copy.deepcopy(self.values)

        obj = Combination(values)

        return obj
