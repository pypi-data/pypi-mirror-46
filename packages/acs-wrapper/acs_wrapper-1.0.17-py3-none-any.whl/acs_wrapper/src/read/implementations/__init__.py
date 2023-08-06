__author__ = 'diegopinheiro'
__email__ = 'diegompin@gmail.com'
__github__ = 'https://github.com/diegompin'

from .acs_read_education import AcsReadEducation
from .acs_read_income import AcsReadIncome
from .acs_read_race import AcsReadRace
from .acs_read_age import AcsReadAge
from .acs_read_total_population import AcsReadTotalPopulation
from .acs_read_type_health_insurance_age import AcsReadTypeHealthInsuranceAge

ALL_IMPLEMENTATIONS = [
    AcsReadEducation,
    AcsReadIncome,
    AcsReadRace,
    AcsReadAge,
    AcsReadTotalPopulation,
    AcsReadTypeHealthInsuranceAge
]
