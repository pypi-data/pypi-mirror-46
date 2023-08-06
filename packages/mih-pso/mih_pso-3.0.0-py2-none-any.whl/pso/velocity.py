# encoding: utf-8

import numpy as np

np.random.seed(42)


from value import DValues



class Velocity(object):

    def __init__(self, omega1, phi1, phi2, omega2, phi3, phi4, lb, ub, rlb, rub, method=None):
        self.omega1 = omega1
        self.phi1   = phi1
        self.phi2   = phi2

        self.omega2 = omega2
        self.phi3   = phi3
        self.phi4   = phi4

        self.lb     = lb
        self.ub     = ub

        self.rlb    = rlb
        self.rub    = rub

        self.method = method


    def init_single(self, vps):
        vel = vps.copy()

        t = vel.vps[0].v.v * self.omega1
        l = max(vel.vps[0].v.v-t, vel.vps[0].v.lb)
        h = min(vel.vps[0].v.v+t, vel.vps[0].v.ub)
        vel.vps[0].v.v = np.random.uniform(l, h, 1)[0]

        # vel.vps[0].v.v = vel.vps[0].v.random()

        return vel



    def create_single(self, vt_vps, vps, vps_best_particle, vps_best_swarm):
        """
        Parameters
        ----------
        vt_vps : Values
            v[t]

        vps : list[ValuePair]
            with one element only

        vps_best_particle : list[ValuePair]

        vps_best_swarm : list[ValuePair]

        Returns
        -------
        vel : Values
            contains vps, list[ValuePair]
        """


        p = self.phi1 * self.r1 * (vps_best_particle.swv - vps.swv)
        g = self.phi2 * self.r2 * (vps_best_swarm.swv    - vps.swv)

        # velocity[t+1] in bound.
        vp = vps.vps[0]
        l = (vp.v.lb - vp.v.v - p - g) / self.omega1
        h = (vp.v.ub - vp.v.v - p - g) / self.omega1

        # TODO: add v[t]
        v = np.random.uniform(l, h, 1)[0]

        v = self.omega1 * v + p + g

        vel = vps.copy()
        vel.vps[0].v.v = v

        return vel



    def init_combination(self, vps):

        cnt = 0

        while(True):

            vel = vps.copy()
            vel.w = [vp.w.random() for vp in vps.vps]
            vel.v = [0 for i in range(len(vps.wv))]

            # velocity[t+1] in bound, at least one w exist
            # vel = vel + vps

            # print vps.w, vel.w
            # print self.lb, self.ub, self.rlb, self.rub, vps.r, vel.r
            # print

            cnt += 1

            if 10 == cnt:
                return vel

            if self.lb <= sum(vel.w) \
            and self.ub >= sum(vel.w) \
            and self.rlb <= vel.r \
            and self.rub >= vel.r:
                # print vps.w, vel.w
                # print self.lb, self.ub, self.rlb, self.rub, vps.r, vel.r
                # print

                # print '-' * 50
                # print
                return vel
        

    
    def random_combination(self, arr, top):
        idx = np.arange(len(arr))
        np.random.shuffle(idx)
        arr[idx[:len(arr)-top]] = 0

        return arr



    def create_combination(self, vt_vps, vps, vps_best_particle, vps_best_swarm):
        """
        Parameters
        ----------
        vt_vps : Values
            v[t]

        vps : Values, list[ValuePair]
            with more than one element

        vps_best_particle : Values, list[ValuePair]

        vps_best_swarm : Values, list[ValuePair]

        Returns
        -------
        vel : Values
            contains vps, list[ValuePair]
        """

        cnt = 0

        while(True):

            p = self.random_combination(np.array(vps_best_particle.w) - np.array(vps.w), self.phi3)
            g = self.random_combination(np.array(vps_best_swarm.w)    - np.array(vps.w), self.phi4)

            v = np.array(vt_vps.w)
            v = (v + p + g).tolist()

            vel = vps.copy()
            vel.w = v
            vel.v = [0 for i in range(len(vps.wv))]

            cnt += 1

            if 10 == cnt:
                return vel

            # velocity[t+1] in bound, at least one w exist
            # when vel is all 1, like [1, 1, 1, 1] not working well
            vel_temp = vel + vps

            # print vps.w, vel.w, vel_temp.w
            # # print self.lb, self.ub, self.rlb, self.rub, vps.r, vel.r, vel_temp.r
            # print self.lb, self.ub, self.rlb, self.rub, vps.r, vel_temp.r
            # print

            if self.lb <= sum(vel_temp.w) \
            and self.ub >= sum(vel_temp.w) \
            and self.rlb <= vel_temp.r \
            and self.rub >= vel_temp.r:
                # print vps.w, vel.w, vel_temp.w
                # print self.lb, self.ub, self.rlb, self.rub, vps.r, vel.r, vel_temp.r
                # print

                # print '-' * 50

                return vel


    def init(self, state):

        dvps = {}

        for name, vps in state.mutable.dvps.iteritems():

            # print name, vps

            if 1 == len(vps.vps):
                dvps[name] = self.init_single(vps)
            else:
                dvps[name] = self.init_combination(vps)


        return DValues(dvps)



    def create(self, particle, state_best_particle, state_best_swarm):
        """
        Parameters
        ----------
        particle : Particle

        state_best_particle : State

        state_best_swarm : State

        Returns
        -------
        vel : DValues
            contains vps, dict{list[ValuePair]}
        """

        self.r1 = np.random.uniform(0,1,1)[0]
        self.r2 = np.random.uniform(0,1,1)[0]

        dvps = {}

        for name, vps in particle.state.mutable.dvps.iteritems():

            if 1 == len(vps.vps):
                dvps[name] = self.create_single(particle.velocity[name], vps,
                             state_best_particle.mutable[name],
                             state_best_swarm.mutable[name])
            else:
                dvps[name] = self.create_combination(particle.velocity[name], vps,
                             state_best_particle.mutable[name],
                             state_best_swarm.mutable[name])


        return DValues(dvps)
