#!/usr/bin/env python
# encoding: utf-8

class BayesianAverageModel():
    """
    Bayesian Model Averaging Method for top ranking

    .. math::
        S = \\frac{C\\times m+\\sum_{i=1}^{n}x_i}{n+C}

    上式中，
    :math:`C` 是一个常数
    :math:`m` 是指标平均值，
    :math:`n` 是目前该项目拥有的评价人数，
    :math:`x_i` 是第 :math:`i` 个评分值。

    :param int c_value: contant of threshold

    """
    def __init__(self, c_value):
        self.c_value = c_value


    def fit(self, m, n, sum_ratings):
        """
        calculate the score

        :param float m: ave of all ratings
        :param int n: number of ratings of this item
        :param float sum_ratings: sum of all ratings of this item

        :return: final score of BMA
        :rtype: float
        """

        return (self.c_value * m + sum_ratings) / (n+self.c_value)
