__author__ = 'diegopinheiro'
__email__ = 'diegompin@gmail.com'
__github__ = 'https://github.com/diegompin'

from acs_wrapper.src.read.acs_read_base import AcsRead


class AcsReadEducation(AcsRead):

    # def __init__(self, datapath, year, estimates):
    def __init__(self, datapath):
        # super().__init__(datapath=datapath, prefix='EDU', datafile='S1501', year=year, estimates=estimates,
        #                  column_format='HC01_EST_VC%02d', is_percent=False)
        super().__init__(datapath=datapath, prefix='EDU', datafile='S1501', column_format='HC01_EST_VC%02d',
                         is_percent=False)

    def get_mappings(self):
        """
        HC01_EST_VC02
        Total; Estimate; Population 18 to 24 years

        HC01_EST_VC03
        Total; Estimate; Population 18 to 24 years - Less than high school graduate

        HC01_EST_VC04
        Total; Estimate; Population 18 to 24 years - High school graduate (includes equivalency)

        HC01_EST_VC05
        Total; Estimate; Population 18 to 24 years - Some college or associate's degree

        HC01_EST_VC06
        Total; Estimate; Population 18 to 24 years - Bachelor's degree or higher

        HC01_EST_VC08
        Total; Estimate; Population 25 years and over

        HC01_EST_VC09
        Total; Estimate; Population 25 years and over - Less than 9th grade

        HC01_EST_VC10
        Total; Estimate; Population 25 years and over - 9th to 12th grade, no diploma

        HC01_EST_VC11
        Total; Estimate; Population 25 years and over - High school graduate (includes equivalency)

        HC01_EST_VC12
        Total; Estimate; Population 25 years and over - Some college, no degree

        HC01_EST_VC13
        Total; Estimate; Population 25 years and over - Associate's degree

        HC01_EST_VC14
        Total; Estimate; Population 25 years and over - Bachelor's degree

        HC01_EST_VC15
        Total; Estimate; Population 25 years and over - Graduate or professional degree
        """

        mappings = [
            {
                'TOTAL': [2],
                'ELEMENTAR': [3],
                'HIGH': [4],
                'COLLEGE': [5],
                'BACHELOR': [6]
            },
            {
                'TOTAL': [8],
                'ELEMENTAR': [9],
                'HIGH': [10, 11],
                'COLLEGE': [12],
                'BACHELOR': [13, 14, 15]
            }
        ]
        return mappings
