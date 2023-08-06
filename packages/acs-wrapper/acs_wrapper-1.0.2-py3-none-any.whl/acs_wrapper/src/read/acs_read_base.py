"""
Author: Diego Pinheiro
github: https://github.com/diegompin

"""
import pandas as pd
import itertools


class AcsRead(object):
    # __COLUMN_GEO__ = 'GEO.display-label'
    __COLUMN_GEO__ = 'GEO.id2'
    __ENCODING__ = "ISO-8859-1"

    # def __init__(self, datapath, prefix, datafile, year=2016, estimates=5, column_format='HC01_EST_VC%02d', is_percent=False):
    def __init__(self, datapath, prefix, datafile, column_format='HC01_EST_VC%02d',
                     is_percent=False):
        self.datapath = datapath
        self.prefix = prefix
        self.datafile = datafile
        # self.year = year
        # self.estimates = estimates
        self.column_format = column_format
        self.is_percent = is_percent

    def get_mappings(self):
        """
        Each class should override this method with the respective mapping
        :return:
        """
        pass

    def get_data(self, level, year, estimates):
        df = self.read_file(level, year, estimates)
        df = self._extract_group_mappings(df)
        df = self._filter_columns(df)
        return df

    # def read_file(self):
    def read_file(self, level, year, estimates):
        df = pd.read_csv(self._get_filename(level, year, estimates), encoding=self.__ENCODING__)
        # Eliminates the first line which is a description of the colunm
        df = df.loc[1:, :]
        # Extract only the zip code such as '00601' from 'ZCTA5 00601'
        # df.loc[:, 'SPATIAL'] = df.loc[:, self.__COLUMN_GEO__].apply(lambda cell: cell if cell.split(' ')[0] != 'ZCTA5' else cell.split(' ')[1] )
        df.loc[:, 'SPATIAL'] = df.loc[:, self.__COLUMN_GEO__]
        # Set the index
        df = df.set_index('SPATIAL')
        return df

    def _get_column_name(self, columns):
        if not isinstance(columns, list):
            column_format = self.column_format
            return [column_format % columns]
        columns_list = [self._get_column_name(c) for c in columns]
        return list(itertools.chain(*columns_list))

    def _extract_group_mappings(self, df):
        mappings = self.get_mappings()
        assert mappings is not None, 'No mapping provided'
        df = df.copy(deep=True)
        # TODO Generalize file output
        for m in mappings[0]:
            df.loc[:, m] = 0
        for group_mapping in mappings:
            df_group = df.copy(deep=True)
            for m in group_mapping:
                columns_group = self._get_column_name(group_mapping[m])
                # Summing the columns belonging to the same group
                df_group.loc[:, m] = df_group.loc[:, columns_group].apply(pd.to_numeric, errors='coerce').sum(axis=1)
            # Multiply the percentages by the total
            if self.is_percent:
                # Divide by 100 the percentages in df_group (i.e., 45.6 -> .456) and multiply by the total
                columns = list(mappings[0].keys())
                df_group = df_group[columns]
                columns_except_total = df_group.columns != 'TOTAL'
                df_group.loc[:, columns_except_total] = (df_group.loc[:, columns_except_total] / 100).multiply(
                    df_group['TOTAL'].values, axis=0)

            for m in group_mapping:
                df.loc[:, m] += df_group.loc[:, m]
        return df

    def _filter_columns(self, df):
        mappings = self.get_mappings()
        prefix = self.prefix
        # Filter only the columns of interest, i.e., mapping.keys()
        df = df[list(mappings[0].keys())]
        # Rename the columns by adding the prefix, e.g. WHITE -> RAC_WHITE
        df.columns = ['%s_%s' % (prefix, c) for c in df.columns]
        return df

    def _get_filename(self, level, year, estimates):
        # return 'datalink/acs_wrapper/data_input/ACS_%d_%dYR_%s_with_ann.csv' % (self.year, self.estimates, self.datafile)
        return f'{self.datapath}/{level}/ACS_{year}_{estimates}YR_{self.datafile}_with_ann.csv'

