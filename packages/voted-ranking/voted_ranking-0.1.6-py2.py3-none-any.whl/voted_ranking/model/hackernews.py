#!/usr/bin/env python
# encoding: utf-8

import arrow


class HackerNewsModel(object):
    """
    Hacker News Model

    如果只有单一决策变量，使用HackerNews是一个不错的方案，默认的Gravityth Power为1.8，更大的值会让分数随时间降低得更快。

    .. math::
        S = \\frac{P-1}{(T+2)^G}

    :param float gravity: gravityth power, it's optional, default value is 1.8

    """

    def __init__(self, gravity=1.8):
        assert gravity > 0
        self.gravity = gravity

    def fit(self, ups, date_created, date_now=None):
        """
        calculate the score

        :param int ups: number of votes
        :param str date_created: post date created
        :return: final score
        :rtype: float

        """
        assert ups > 1
        assert type(date_created) == str

        if date_now is None:
            date_now = arrow.now()
        else:
            date_now = arrow.get(date_now)

        T = (date_now - arrow.get(date_created)).total_seconds() / 3600

        return (ups - 1) / ((T+2) ** self.gravity)
