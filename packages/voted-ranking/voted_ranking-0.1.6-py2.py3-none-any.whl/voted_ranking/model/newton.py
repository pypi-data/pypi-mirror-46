#!/usr/bin/env python
# encoding: utf-8

import math
import arrow


class NewtonCoolingModel(object):
    """
    Newton Cooling Model, based on exponential decay

    .. math::
        S_1 = S_0e^{\\alpha(t_1-t_0)}

    基于时间指数衰减的牛顿冷却，这里的 :math:`alpha` 是冷却系数，越大的冷却系数会让分数衰减得更快。

    """

    def __init__(self, alpha=0.1, init_temp=0):
        self.alpha = alpha
        self.init_temp = init_temp


    def fit(self, score, score_time, date_now=None):
        """
        calculate the score after decay

        :param float score: the score before decay
        :param str score_time: time before decay "2019-04-15 12:20:20"
        :param str date_now: time after decay, default is arrow.now
        :return: score after decay
        :rtype: float

        """
        if date_now is None:
            date_now = arrow.now()
        else:
            date_now = arrow.get(date_now)

        hours = (date_now - arrow.get(score_time)).total_seconds() / 3600
        decay_factor = hours * (-self.alpha)
        score = self.init_temp + (score-self.init_temp ) * math.e ** decay_factor
        return score
