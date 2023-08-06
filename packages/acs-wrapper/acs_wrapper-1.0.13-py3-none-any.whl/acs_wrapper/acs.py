"""
Author: Diego Pinheiro
github: https://github.com/diegompin

"""

import pandas as pd


class Acs(object):

    __DATAPATH__ = '%s/df_AcsRead%s_%s_%d_%d.csv'

    def __init__(self, data_path='data/data_output'):
        self.datapath = data_path

    def _get_df_(self, datapath, normed=False):
        df = pd.read_csv(datapath)
        df = df.set_index('SPATIAL')
        column_total = df.columns[df.columns.str.endswith('_TOTAL')][0]
        if normed:
            df.loc[:, df.columns != column_total] = df.loc[:, df.columns != column_total].apply(lambda r: r / df[column_total], axis=0)
        df = df.dropna()
        return df

    def get_race(self, level, year, estimate, normed=False):
        datapath = self.__DATAPATH__ % (self.datapath, 'Race', level, year, estimate)
        df = self._get_df_(datapath, normed)
        return df

    def get_education(self, level, year, estimate, normed=False):
        datapath = self.__DATAPATH__ % (self.datapath, 'Education', level, year, estimate)
        df = self._get_df_(datapath, normed)
        return df

    def get_income(self, level, year, estimate, normed=False):
        datapath = self.__DATAPATH__ % (self.datapath, 'Income', level, year, estimate)
        df = self._get_df_(datapath, normed)
        return df

    def get_acs(self, level, year, estimate, normed=False):
        # Read individual files
        df_race = self.get_race(level, year, estimate, normed)
        df_education = self.get_education(level, year, estimate, normed)
        df_income = self.get_income(level, year, estimate, normed)
        # Merge pairs of files
        df = pd.merge(df_race, df_education, left_index=True, right_index=True)
        df = pd.merge(df, df_income, left_index=True, right_index=True)
        return df

    # def get_implementations(self):
    #     dict_area_function = {
    #         'race': None,
    #         'education': None,
    #         'income': None
    #     }
    #     return dict_area_function
    #
    #
    # def get_data(self, data_name):
    #         dict_data_function = self.get_implementations()
    #         assert data_name in dict_data_function, 'area not implemented'
    #         data = dict_data_function[data_name]
    #         method_to_call = getattr(data(), 'get_data')
    #         return method_to_call()
