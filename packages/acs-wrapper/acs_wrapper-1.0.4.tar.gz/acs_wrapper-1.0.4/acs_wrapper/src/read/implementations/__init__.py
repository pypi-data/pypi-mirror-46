__author__ = 'diegopinheiro'
__email__ = 'diegompin@gmail.com'
__github__ = 'https://github.com/diegompin'

from .acs_read_education import AcsReadEducation
from .acs_read_income import AcsReadIncome
from .acs_read_race import AcsReadRace
from .acs_read_age65 import AcsReadAge65
from .acs_read_total_population import AcsReadTotalPopulation

ALL_IMPLEMENTATIONS = [
    AcsReadEducation,
    AcsReadIncome,
    AcsReadRace,
    AcsReadAge65,
    AcsReadTotalPopulation
]
