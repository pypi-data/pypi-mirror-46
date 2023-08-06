# encoding: utf-8

from collections import OrderedDict


class State(OrderedDict):


    def copy(self):

        obj = State()

        for k, v in self.iteritems():

            obj[k] = v.copy()

        return obj



    def action(self):

        map(lambda (k, v): v.action(), self.iteritems())



    def refresh(self, lbest_state, gbest_state):

        map(lambda (k, v): v.refresh(lbest_state[k].v, gbest_state[k].v), self.iteritems())



    def to_series(self):

        # TODO:

        pass
