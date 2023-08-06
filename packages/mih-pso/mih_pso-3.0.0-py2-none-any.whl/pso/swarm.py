# encoding: utf-8

from progressbar import progressbar


class Swarm(object):

    """ Particle Swarm Optimization
    
    """

    def __init__(self, particles, max_iter=100):
        """
        Parameters
        ----------
        particles : list[Particle]

        max_iter : int, default 100
        """

        self.max_iter       = max_iter
        self.particles      = particles

        self.refresh()


    def refresh(self):
        """ update gbest of swarm and particles

        Parameters
        ----------
        self.particles : list[Particle]

        Returns
        -------
        self.gbest_particle : Particle
        """

        self.gbest_particle = reduce(lambda p1, p2: p1.compare(p2), self.particles)

        map(lambda p: p.refresh(self.gbest_particle.lbest_state), self.particles)


    def optimize(self):

        for i in range(self.max_iter):

            map(lambda p: p.action(), self.particles)
            self.refresh()
