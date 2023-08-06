__author__ = 'diegopinheiro'
__email__ = 'diegompin@gmail.com'
__github__ = 'https://github.com/diegompin'

from acs_wrapper.src.read.acs_read_base import AcsRead


class AcsReadRace(AcsRead):

    def __init__(self, datapath):
        super().__init__(datapath=datapath, prefix='RAC', datafile='B03002', column_format='HD01_VD%02d',
                         is_percent=False)

    def get_mappings(self):
        """
        HD01_VD03
        Estimate; Not Hispanic or Latino: - White alone

        HD01_VD04
        Estimate; Not Hispanic or Latino: - Black or African American alone
        """
        mappings = [{
            'TOTAL': 1,
            'WHITE': 3,
            'BLACK': 4,
            'INDIAN': 5,
            'ASIAN': 6,
            'PACIFIC': 7,
            'OTHER': [8, 9],
            'HISPANIC': [13, 14, 15, 16, 17, 18, 19]
        }]
        return mappings
