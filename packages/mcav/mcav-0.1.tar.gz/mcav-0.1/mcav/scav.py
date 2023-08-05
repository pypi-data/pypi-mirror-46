import math


class SCAV(object):
    # realize the SCA algorithm
    def __init__(self, amount, size, popurity_dict, rate, time):
        self._amount = amount
        self._size = size
        self._alpha = popurity_dict
        self._P = {}
        # self._P[1] = self._alpha
        self._B = {}
        self._request_rate = rate
        self._staleness_time = time
        self._validation_rate = self._validationRate()
        self._validation_probability = self._validationProbability()
        self._P[1] = self._computeP1()
        self._hitRatio()

    def hitRatio(self):
        return self._B[self._size]

    def totalHitRatio(self):
        total_hit_ratio = 0.0
        for i in range(1, self._amount+1):
            total_hit_ratio = total_hit_ratio + \
                self._alpha[i]*self._B[self._size][i]
        return total_hit_ratio

    def _hitRatio(self):
        for i in range(1, self._size + 1):
            self._computeB(i)
            i = i + 1
            if i <= self._size:
                self._computeP(i)

    def _computeP(self, position):
        # position starts from 2
        p = {}
        molecule = []
        denominator = 0.0
        for i in range(1, self._amount + 1):
            denominator = denominator + \
                self._nonNegative(
                    self._alpha[i] * (1 - self._B[position-1][i]))
        for i in range(1, self._amount + 1):
            molecule = self._nonNegative(
                self._alpha[i] * (1 - self._B[position-1][i]))
            p[i] = self._validation_probability[i] * molecule / denominator

        self._P[position] = p
        # print p
        # print sum(p.values())
        # print "-----=------"

    def _computeB(self, position):
        # position starts from 1
        b = {}
        for i in range(1, self._amount + 1):
            b[i] = 0.0
            for j in range(1, position + 1):
                b[i] = b[i] + self._P[j][i]
        self._B[position] = b

    def _nonNegative(self, number):
        if number > 0:
            return number
        else:
            return 0.0

    def _validationProbability(self):
        vp = {}
        for i in range(1, self._amount + 1):
            vp[i] = 1 - math.pow(math.e, - self._alpha[i]
                                 * self._validation_rate * self._staleness_time)
        return vp

    # def _validationRate(self):
    #     validation_rate = self._request_rate * \
    #         (1 - math.pow(math.e, - self._staleness_time / self._size))
    #     return validation_rate

    def _validationRate(self):
        validation_rate = self._request_rate * \
            math.pow(math.e, - self._size /
                     self._staleness_time/self._request_rate)
        return validation_rate

    def _computeP1(self):
        P1 = {}
        for i in range(1, self._amount + 1):
            P1[i] = self._alpha[i] * self._validation_probability[i]
        return P1
