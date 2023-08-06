#!/usr/bin/env python
# encoding: utf-8

import numpy as np

class WilsonGaussianModel():
    """
    Wilson Gaussion Model

    .. math::
        S = \\frac{\\mu+\\frac{z^2}{2n}-\\frac{z}{2n}\\sqrt{4n\\sigma^2+z^2}}{1+\\frac{z^2}{n}}, \\mu\\in(0,1), \\sigma\\in(0,1)

    .. note::
        基于高斯分布的威尔逊得分和基于伯努利分布的威尔逊得分区别算法上不大，
        只是将原来的click or not / like or not的二项分布换成高斯分布，
        适用于多级评分值的业务场景。

    :param float z_value: z value of confidence interval, default is 1.96 of 95% :class:`numpy.ndarray`

    """
    def __init__(self, z_value=1.96):
        self.z_value = z_value

    def fit(self, mean, var, total):
        """
        calculate the wilson score for gaussion distribution

        .. warning::
            需要注意使用高斯分布威尔逊得分时，均值和方差一定要先做归一化转换，可以选择 :math:`min\_max` 归一化，:math:`log` 归一化，:math:`\\arctan` 归一化。

        :param float mean: mean of metric value which transformed to 0~1
        :param float variance: variance of metric value which transformed to 0~1
        :return: wilson score for guassion distribution
        :rtype: float

        """

        score = (mean + (np.square(self.z_value) / (2. * total))
                 - ((self.z_value/ (2. * total)) * np.sqrt(4. * total * var + np.square(self.z_value)))) / \
                    (1 + np.square(self.z_value) / total)

        return score


class WilsonBernolliModel():
    """
    Wilson Bernolli Model

    .. math::
        S = \\frac{p + \\frac{z^2}{2n} - z\\sqrt{\\frac{p(1-p)}{n} + \\frac{z^2}{4n^2} }}{1+\\frac{z}{n}}

    .. note::
        基于伯努利分布的威尔逊得分，适用于click or not / like or not的二项分布投票场景。

    :param float z_value: z value of confidence interval, default is 1.96 of 95%

    """
    def __init__(self, z_value=1.96):
        self.z_value = z_value


    def fit(self, ups, total):
        """
        calculate the wilson score for bernolli distribution

        :param int ups: number of postive votes
        :param int total: number of total votes / post views

        :return: wilson score
        :rtype: float

        """

        assert total >= ups

        up_ratio = ups * 1. / total * 1.
        score = (up_ratio + (np.square(self.z_value) / (2. * total))
                 - ((self.z_value / (2. * total)) * np.sqrt(4. * total * (1. - up_ratio) * up_ratio + np.square(self.z_value)))) / \
                (1. + np.square(self.z_value) / total)
        return score
