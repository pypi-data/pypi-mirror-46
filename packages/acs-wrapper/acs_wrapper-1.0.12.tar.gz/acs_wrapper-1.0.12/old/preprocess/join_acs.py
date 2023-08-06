"""
Author: Diego Pinheiro
github: https://github.com/diegompin

"""

from acs_wrapper import Acs
import pandas as pd

def main(datalink_acs='datalink/acs_wrapper', level='zcta'):
    df_rac = pd.read_csv('%s/data_output/df_AcsReadRace_%s_16_5.csv' % (datalink_acs, level), index_col=0)
    df_edu = pd.read_csv('%s/data_output/df_AcsReadEducation_%s_16_5.csv' % (datalink_acs, level), index_col=0)
    df_inc = pd.read_csv('%s/data_output/df_AcsReadIncome_%s_16_5.csv' % (datalink_acs, level), index_col=0)
    df_rac = df_rac.loc[:, df_rac.columns != 'RAC_TOTAL'].apply(lambda r: r / df_rac['RAC_TOTAL'], axis=0)
    df_edu = df_edu.loc[:, df_edu.columns != 'EDU_TOTAL'].apply(lambda r: r / df_edu['EDU_TOTAL'], axis=0)
    df_inc = df_inc.loc[:, df_inc.columns != 'INC_TOTAL'].apply(lambda r: r / df_inc['INC_TOTAL'], axis=0)
    # join
    df = df_rac.join(df_edu)
    df = df.join(df_inc)
    df = df.dropna(axis=0)
    # TODO generalize
    # filename_output = 'acs_wrapper/data_output/acs_%d_%d.hdf' % (16, 5)
    filename_output = 'datalink/acs_wrapper/data_output/acs_%d_%d_%s.csv' % (16, 5, level)
    df.to_csv(filename_output)


if __name__ == "__main__":
    main()


# datalink_acs='datalink/acs_wrapper'
# df_rac = pd.read_csv('%s/data_output/df_AcsReadRace_county_16_5.csv' % datalink_acs)
# df_edu = pd.read_csv('%s/data_output/df_AcsReadEducation_county_16_5.csv' % datalink_acs)
# df = df_rac.merge(df_edu, how='inner', left_index=True, right_index=True)