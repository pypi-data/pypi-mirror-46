__author__ = 'diegopinheiro'
__email__ = 'diegompin@gmail.com'
__github__ = 'https://github.com/diegompin'

from acs_wrapper.src.read.acs_read_base import AcsRead


class AcsReadAge65(AcsRead):

    def __init__(self, datapath):
        super().__init__(datapath=datapath, prefix='AGE65', datafile='S0103', column_format='HC%02d_EST_VC01',
                         is_percent=False)

    def get_mappings(self):
        mappings = [
            {
                'TOTAL': [1],
                'OVER65': [2]
            }
        ]
        return mappings
