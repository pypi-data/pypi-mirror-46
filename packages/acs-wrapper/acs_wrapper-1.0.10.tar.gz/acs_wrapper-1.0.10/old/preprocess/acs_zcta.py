"""
Author: Diego Pinheiro
github: https://github.com/diegompin

"""

import pandas as pd
import itertools as it
from old.script import AcsPreprocess


def main():
    data_path_acs = 'datalink/acs_wrapper/data_output'
    data_path_spatial = 'datalink/spatial/data_output'
    filepath_zcta = '%s/zcta_county_state.hdf' % data_path_spatial
    readers, year, estimates = AcsPreprocess.get_param()

    df_spatial = pd.read_hdf('%s/zcta_county_state.hdf' % data_path_spatial)

    for (r, y, e) in it.product(readers, year, estimates):
        df_acs = pd.read_csv('%s/%s_%d_%d.csv' % (data_path_acs, r.__name__, y, e))


if __name__ == "__main__":
    main()

# len(df_spatial.ZIP.unique())