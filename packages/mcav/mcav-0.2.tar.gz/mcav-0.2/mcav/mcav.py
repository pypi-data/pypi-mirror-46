from scav import SCAV

class MCAV(object):
    # realize the MCA algorithm
    def __init__(self, amount, size, popularity_dict, rate, time, miss_rate={}):
        self._amount = amount
        self._size = size
        self._popularity = popularity_dict
        self._staleness_time = time
        self._rate = rate   # a number
        self._miss_rate = miss_rate # a dict

        self._total_rate = self._totalRate()
        self._request_probability = self._requestProbability()
        self._sca_validation = SCAV(amount, size, self._request_probability, sum(self._total_rate.values()), time)
        # self._sca = SCA(amount, size, self._request_probability)
        self._hit_ratio = self._sca_validation.hitRatio()
        # self._hit_ratio_sca = self._sca.hitRatio()

    def hitRatio(self):
        return self._hit_ratio

    def totalHitRatio(self):
        h = 0
        for i in range(1, self._amount + 1):
            h = h + self._request_probability[i] * self._hit_ratio[i]
        return h

    def missRate(self):
        m = {}
        for i in range(1, self._amount + 1):
            m[i] = self._total_rate[i] * (1 - self._hit_ratio[i])
        return m

    def _totalRate(self):
        r = {}
        if self._miss_rate:
            for i in range(1, self._amount + 1):
                r[i] = self._rate * self._popularity[i] + self._miss_rate[i]
        else:
            for i in range(1, self._amount + 1):
                r[i] = self._rate * self._popularity[i]
        return r

    def _requestProbability(self):
        p = {}
        for i in range(1, self._amount + 1):
            p[i] = self._total_rate[i] / sum(self._total_rate.values())
        return p