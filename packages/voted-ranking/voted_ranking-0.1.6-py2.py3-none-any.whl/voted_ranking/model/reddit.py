#!/usr/bin/env python
# encoding: utf-8

import arrow
import math


class RedditModel():
    """
    Reddit Topic Ranking Model

    .. math::
        S = log_{10}z + \\frac{y\\Delta t}{45000}

        y = \\begin{cases}
            1 & \\text(x>0) \\\\
            0 & \\text(x=0) \\\\
            -1 & \\text(x<0)
            \\end{cases}

        z = \\begin{cases}
            |x| & \\text{if x≠0} \\\\
            1 & \\text{if x = 0}
            \\end{cases}


    .. note::
        Reddit的帖子排序，如果你同时需要支持和反对票，同时新鲜度非常重要，那么它可能是适合的模型。

    :param str date_init: init date to calculdate the time score, default is '2010-01-01 00:00:00'. It's optional

    """

    def __init__(self, date_init="2019-05-01 00:00:00"):
        self.date_init = date_init

    def fit(self, ups, downs, date_created):
        """
        calculate the score

        :param int ups: number of postive votes
        :param int downs: number of negative votes
        :param str date_created: post date created
        :return: final score
        :rtype: float

        """
        x = ups - downs
        if x > 0:
            y = 1
        elif x < 0:
            y = -1
        else:
            y = 0

        if x == 0:
            z = 1
        else:
            z = abs(x)

        t = (arrow.get(date_created) - arrow.get(self.date_init)).total_seconds()
        score = math.log10(z) + y * t / 45000
        return score
