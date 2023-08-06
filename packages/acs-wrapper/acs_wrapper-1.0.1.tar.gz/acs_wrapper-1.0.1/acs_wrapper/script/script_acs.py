"""
Author: Diego Pinheiro
github: https://github.com/diegompin

"""

from acs_wrapper.script.common import ScriptBase
from acs_wrapper.acs import Acs
import pandas as pd
import itertools as it


class ScriptAcs(ScriptBase):
    def __init__(self, par):
        super().__init__(par)

    def get_file_output(self, params):
        (df, xvar, yvar) = params
        data_link_output = self.data_link_output
        file_output = '%s/US/%s__%s__%s.pdf' % (data_link_output, self.name, xvar, yvar)
        print(file_output)
        return file_output

    def get_params(self):

        estimate = 5
        year = 16
        level = 'county'

        acs = Acs()
        normed = True
        df_race = acs.get_race(level, year, estimate, normed=normed)
        df_education = acs.get_education(level, year, estimate, normed=normed)
        df_income = acs.get_income(level, year, estimate, normed=normed)
        df = pd.merge(df_race, df_education, left_index=True, right_index=True)
        df = pd.merge(df, df_income, left_index=True, right_index=True)
        cols = [c for c in df.columns if not c.endswith('_TOTAL')]
        df = df[cols]
        # cols = [c.split('_')[1].title() for c in cols]
        # df.columns = cols
        # mapping_income = {'A': '10k', 'B': '10k-15k', 'C': '15k-25k', 'D': '25k-35k',
        #                   'E': '35k-50k', 'F': '50k-75k', 'G': '75k-100k', 'H': '100k-150k', 'I': '150k-200k',
        #                   'J': '200k'}
        # df = df.rename(columns=mapping_income)

        # return [(df, c1, c2) for (c1,c2) in it.combinations(df.columns[0:3], r=2)]
        return it.product([df], df.columns, [c for c in df.columns if c.endswith('ELEMENTAR')])
        # return it.product([df], df.columns, df.columns)

