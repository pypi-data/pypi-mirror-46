__author__ = 'diegopinheiro'
__email__ = 'diegompin@gmail.com'
__github__ = 'https://github.com/diegompin'

from acs_wrapper.src.read.acs_read_base import AcsRead


class AcsReadAge(AcsRead):

    def __init__(self, datapath):
        super().__init__(datapath=datapath, prefix='AGE', datafile='S0101', column_format='HC01_EST_VC%02d',
                         is_percent=False)

    def get_mappings(self):
        """
        HC01_EST_VC01
        Total; Estimate; Total population

        HC01_EST_VC03
        Total; Estimate; AGE - Under 5 years

        HC01_EST_VC04
        Total; Estimate; AGE - 5 to 9 years

        HC01_EST_VC05
        Total; Estimate; AGE - 10 to 14 years

        HC01_EST_VC06
        Total; Estimate; AGE - 15 to 19 years

        HC01_EST_VC07
        Total; Estimate; AGE - 20 to 24 years

        HC01_EST_VC08
        Total; Estimate; AGE - 25 to 29 years

        HC01_EST_VC09
        Total; Estimate; AGE - 30 to 34 years

        HC01_EST_VC10
        Total; Estimate; AGE - 35 to 39 years

        HC01_EST_VC11
        Total; Estimate; AGE - 40 to 44 years

        HC01_EST_VC12
        Total; Estimate; AGE - 45 to 49 years

        HC01_EST_VC13
        Total; Estimate; AGE - 50 to 54 years

        HC01_EST_VC14
        Total; Estimate; AGE - 55 to 59 years

        HC01_EST_VC15
        Total; Estimate; AGE - 60 to 64 years

        HC01_EST_VC16
        Total; Estimate; AGE - 65 to 69 years

        HC01_EST_VC17
        Total; Estimate; AGE - 70 to 74 years

        HC01_EST_VC18
        Total; Estimate; AGE - 75 to 79 years

        HC01_EST_VC19
        Total; Estimate; AGE - 80 to 84 years

        HC01_EST_VC20
        Total; Estimate; AGE - 85 years and over

        """
        mappings = [
            {
                'TOTAL': [1],
                'UNDER_05': [3],
                'FROM_05_TO_09': [4],
                'FROM_10_TO_14': [5],
                'FROM_15_TO_19': [6],
                'FROM_20_TO_24': [7],
                'FROM_25_TO_29': [8],
                'FROM_30_TO_34': [9],
                'FROM_35_TO_39': [10],
                'FROM_40_TO_44': [11],
                'FROM_45_TO_49': [12],
                'FROM_50_TO_54': [13],
                'FROM_55_TO_59': [14],
                'FROM_60_TO_64': [15],
                'FROM_65_TO_69': [16],
                'FROM_70_TO_74': [17],
                'FROM_75_TO_79': [18],
                'FROM_80_TO_84': [19],
                'ABOVE_85': [20],

            }
        ]
        return mappings
