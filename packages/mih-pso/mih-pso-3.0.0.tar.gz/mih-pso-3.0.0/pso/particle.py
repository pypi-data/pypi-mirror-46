# encoding: utf-8


class Particle(object):



    def __init__(self, state, scorer):

        self.state       = state
        self.scorer      = scorer

        self.lbest_state = self.state.copy()



    def copy(self):

        state           = self.state.copy()
        lbest_state     = self.lbest_state.copy()

        obj             = Particle(state, self.scorer)
        obj.lbest_state = lbest_state

        return obj



    def action(self):

        self.state.action()

        if self.scorer.compare(self.state, self.lbest_state):
            self.lbest_state = self.state.copy()



    def compare(self, p):

        """ Compare self.lbest_state & p.lbest_state


        Parameters
        ----------
        p : Particle

        Returns
        -------
        best particle: Particle
        """

        if self.scorer.compare(self.lbest_state, p.lbest_state):
            return self.copy()

        return p.copy()



    def refresh(self, gbest_state):

        self.state.refresh(self.lbest_state, gbest_state)
