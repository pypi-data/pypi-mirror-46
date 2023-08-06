# encoding: utf-8

class Scorer(object):

    def __init__(self, metric='min'):
        self.metric = metric


    def score(self, state):
        pass


    def compare(self, state1, state2):
        """
        state1 better than state2
        """

        score1 = self.score(state1)
        score2 = self.score(state2)

        if 'min' == self.metric and score1 < score2:
            return True
        elif 'max' == self.metric and score1 > score2:
            return True

        return False



class Constraint(Scorer):

    def __init__(self, threshold, metric='min'):
        super(Constraint, self).__init__(metric)
        self.threshold = threshold

    def meet(self, state):
        if 'min' == self.metric:
            return self.score(state) < self.threshold
        elif 'max' == self.metric:
            return self.score(state) > self.threshold



class ScorerConstraint(object):

    def __init__(self, scorer, constraint):
        self.scorer     = scorer
        self.constraint = constraint


    def compare(self, state1, state2):
        meet1 = self.constraint.meet(state1)
        meet2 = self.constraint.meet(state2)

        if meet1 and meet2:
            return self.scorer.compare(state1, state2)
        elif meet1:
            return True
        elif meet2:
            return False
        else:
            return self.constraint.compare(state1, state2)
