"""
Author: Diego Pinheiro
github: https://github.com/diegompin

"""

from acs_wrapper.src.read.acs_read_base import AcsRead




#
# datapath = 'data/data_input/%s'
# l = 'county'
# y = 16
# e = 5
# r = AcsReadRace(datapath=datapath % l, year=y, estimates=e)
# r_edu = AcsReadEducation(datapath=datapath % l, year=y, estimates=e)
# r_inc = AcsReadIncome(datapath=datapath % l, year=y, estimates=e)
#
# df_rac = r.get_data()
# df_edu = r_edu.get_data()
# df_inc = r_inc.get_data()
#
#
# df_rac.loc['01001']
# df_edu.loc['01001']
# df_inc.loc['01001']
#
#
# import numpy as np
# np.corrcoef(df_edu.loc[:, 'EDU_TOTAL'].values, df_rac.loc[:, 'RAC_TOTAL'].values)
#
#
