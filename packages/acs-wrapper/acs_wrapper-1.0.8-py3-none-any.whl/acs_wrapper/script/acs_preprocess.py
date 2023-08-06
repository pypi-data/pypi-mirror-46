"""
Author: Diego Pinheiro
github: https://github.com/diegompin

"""

from acs_wrapper.src.read import *


class AcsPreprocess(object):

    def __init__(self):
        pass

    @staticmethod
    def get_param():
        readers = ALL_IMPLEMENTATIONS
        # readers = [
        #     AcsReadRace,
        #     AcsReadEducation,
        #     AcsReadIncome,
        #     AcsReadAge65,
        #
        # ]
        # readers = [AcsReadRace]
        # level = ['county', 'zcta']
        level = ['zcta']

        year = [17]
        estimates = [5]
        return readers, level, year, estimates
