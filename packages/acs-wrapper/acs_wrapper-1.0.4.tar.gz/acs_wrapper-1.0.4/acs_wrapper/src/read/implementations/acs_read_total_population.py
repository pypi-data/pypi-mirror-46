__author__ = 'diegopinheiro'
__email__ = 'diegompin@gmail.com'
__github__ = 'https://github.com/diegompin'

from acs_wrapper.src.read.acs_read_base import AcsRead


class AcsReadTotalPopulation(AcsRead):

    def __init__(self, datapath):
        super().__init__(datapath=datapath, prefix='TOT', datafile='B01003', column_format='HD01_VD%02d')

    def get_mappings(self):
        mappings = [
            {
                'TOTAL_POPULATION': [1]
            }
        ]
        return mappings
