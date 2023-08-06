# encoding: utf-8


import copy
import warnings
import numpy as np

np.random.seed(42)



class Value(object):


    def __init__(self, v):
        self._v       = v

        self.lbest_v = None
        self.gbest_v = None


    @property
    def v(self):
        return self._v


    @v.setter
    def v(self, value):
        self._v = value


    def create(self):
        pass


    def action(self):
        pass


    def refresh(self, lbest_v, gbest_v):
        self.lbest_v = lbest_v
        self.gbest_v = gbest_v


    def copy(self):
        v       = copy.deepcopy(self.v)
        lbest_v = copy.deepcopy(self.lbest_v)
        gbest_v = copy.deepcopy(self.gbest_v)

        obj         = Value(v)
        obj.lbest_v = lbest_v
        obj.gbest_v = gbest_v

        return obj



class ValueNumeric(Value):


    def __init__(self, lbound, ubound, omega, phi1, phi2, v=None):
        self.lbound = lbound
        self.ubound = ubound
        self.omega  = omega
        self.phi1   = phi1
        self.phi2   = phi2

        v = v if v is not None else self.init_value()
        super(ValueNumeric, self).__init__(v)
        self.check_value()

        self.velocity = self.init_velocity()


    @property
    def v(self):
        return self._v


    @v.setter
    def v(self, value):
        self._v = value
        self.check_value()


    def check_value(self):

        if self.v > self.ubound:
            warnings.warn(\
                    'value [%s] greater than upper bound [%s], reset to upper bound'\
                    % (self.v, self.ubound))

            self.v = self.ubound

        elif self.v < self.lbound:
            warnings.warn(\
                    'value [%s] less than lower bound [%s], reset to lower bound'\
                    % (self.v, self.ubound))

            self.v = self.lbound


    def init_value(self):
        return np.random.uniform(self.lbound, self.ubound)


    def init_velocity(self):
        return np.random.uniform(self.lbound-self.v, self.ubound-self.v)


    def create_velocity(self):

        r1 = np.random.uniform(0, 1)
        r2 = np.random.uniform(0, 1)

        self.velocity = self.omega * self.velocity + \
                        self.phi1  * r1 * (self.lbest_v - self.v) + \
                        self.phi2  * r2 * (self.gbest_v - self.v)

        # for test only
        return r1, r2


    def action(self):

        self.create_velocity()
        self.v += self.velocity

        self.v = min(self.ubound, self.v)
        self.v = max(self.lbound, self.v)

        # for test only
        return self.velocity


    def copy(self):
        v        = copy.deepcopy(self.v)
        lbest_v  = copy.deepcopy(self.lbest_v)
        gbest_v  = copy.deepcopy(self.gbest_v)
        lbound   = copy.deepcopy(self.lbound)
        ubound   = copy.deepcopy(self.ubound)
        omega    = copy.deepcopy(self.omega)
        phi1     = copy.deepcopy(self.phi1)
        phi2     = copy.deepcopy(self.phi2)
        velocity = copy.deepcopy(self.velocity)

        obj          = ValueNumeric(lbound, ubound, omega, phi1, phi2, v)
        obj.lbest_v  = lbest_v
        obj.gbest_v  = gbest_v
        obj.velocity = velocity

        return obj



class ValueListBinary(Value):


    def __init__(self, lbound, ubound, omega, phi1, phi2, comb, v=None):
        self.lbound = lbound
        self.ubound = ubound
        self.omega  = omega
        self.phi1   = phi1
        self.phi2   = phi2

        self.comb   = comb

        v = v if v is not None else self.init_value()
        super(ValueListBinary, self).__init__(v)

        self.velocity = self.init_velocity()


    def init_value(self):
        return self.comb.value_of(np.random.randint(self.lbound, self.ubound+1))


    def init_velocity(self):
        v = self.init_value()
        return self.diff_value(v, self.v)


    def pick_random(self, num):
        idx = np.arange(len(self.v))
        np.random.shuffle(idx)

        return idx[:num]


    def replace_velocity(self, values, num):
        idx = self.pick_random(num)

        for i in idx:
            self.velocity[i] += values[i]


    def diff_value(self, v1, v2):
        return (np.array(v1) - np.array(v2)).tolist()


    def create_velocity(self):
        r1 = np.random.randint(1, 2+1)
        r2 = np.random.randint(1, 2+1)

        p1 = int(self.phi1 * r1)
        p1 = min(len(self.v), p1)
        p1 = max(1, p1)

        p2 = int(self.phi2 * r2)
        p2 = min(len(self.v), p2)
        p2 = max(1, p2)

        velocity = copy.deepcopy(self.velocity)

        try:
            self.replace_velocity(self.velocity, self.omega)
            self.replace_velocity(self.diff_value(self.lbest_v, self.v), p1)
            self.replace_velocity(self.diff_value(self.gbest_v, self.v), p2)
        except:
            self.velocity = velocity
            raise

        # for test only
        return r1, r2


    def add_value(self, v1, v2):
        return (np.array(v1) + np.array(v2)).tolist()


    def action(self):

        self.create_velocity()
        self.v = self.add_value(self.v, self.velocity)

        self.v = map(lambda x: 0 if x<=0 else 1, self.v)

        rank = self.comb.rank_of(self.v)
        rank = min(self.ubound, rank)
        rank = max(self.lbound, rank)

        self.v = self.comb.value_of(rank)


    def copy(self):
        v        = copy.deepcopy(self.v)
        lbest_v  = copy.deepcopy(self.lbest_v)
        gbest_v  = copy.deepcopy(self.gbest_v)
        lbound   = copy.deepcopy(self.lbound)
        ubound   = copy.deepcopy(self.ubound)
        omega    = copy.deepcopy(self.omega)
        phi1     = copy.deepcopy(self.phi1)
        phi2     = copy.deepcopy(self.phi2)
        comb     = self.comb.copy()
        velocity = copy.deepcopy(self.velocity)

        obj          = ValueListBinary(lbound, ubound, omega, phi1, phi2, comb, v)
        obj.lbest_v  = lbest_v
        obj.gbest_v  = gbest_v
        obj.velocity = velocity

        return obj
