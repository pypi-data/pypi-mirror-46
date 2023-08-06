#!/usr/bin/env python
# encoding: utf-8

import math
import arrow


class BaseModel(object):
    def __init__(self):
        """
        ssss

        :url: sss
        :return: json
        """
        self.time_score_start = arrow.get('2019-04-15 12:30:45')

    @staticmethod
    def fit(date_created, features):
        """
        created time: "2019-04-15 12:20:20"
        """
        time_score_start = arrow.get(date_created)
        feature_score = sum(features)
        time_score = (arrow.now() - time_score_start).total_seconds()/3600/24 * (-0.6)
        gravity_score = math.e ** time_score
        rank_score = feature_score * gravity_score
        return rank_score


def test():
    """
    this's the function desc

    :url: `hi`
    :method: get

    :return: json



    """

    return None
