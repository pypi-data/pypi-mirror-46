"""
Author: Diego Pinheiro
github: https://github.com/diegompin

"""
import itertools as it
from old.script import AcsPreprocess
from acs_wrapper.src.util_multiprocessing import MyPool


class AcsProcess(object):

    def __init__(self, filepath_input, filepath_output, ):
        self.filepath_input = filepath_input
        self.filepath_output = filepath_output

    def write_hdf(self, args):
        reader, level, year, estimate = args
        reader = reader(self.filepath_input)
        df = reader.get_data(level, year, estimate)
        filename_output = f'{self.filepath_output}/df_{reader.prefix}_{level}_{year}_{estimate}'
        df.to_csv(f'{filename_output}.csv', index=True)
        df.to_hdf(f'{filename_output}.hdf', 'df')

    def process(self):
        list_reader, list_level, list_year, list_estimate = AcsPreprocess.get_param()
        list_args = it.product(list_reader, list_level, list_year, list_estimate)
        with MyPool(processes=4) as pool:
            pool.map(self.write_hdf, list_args)

# def main():
#     print('INITIALIZING EXPORTING ACS DATA')
#     list_reader, list_level, list_year, list_estimate = AcsPreprocess.get_param()
#
#     mod_acs_process = AcsProcess()
#     # data = dict()
#     # for arg in it.product(list_reader, list_level, list_year, list_estimate):
#         # name = reader.__name__.split('AcsRead')[1].lower()
#         # data[f'{name}_{level}_{year}_{estimate}'] = reader(datapath=datapath % level, year=year,
#         #                                                               estimates=estimate)
#     # list_args = tuple(zip(data.keys(), data.values()))
#     list_args = it.product(list_reader, list_level, list_year, list_estimate)
#
#
#     print('FINISHED EXPORTING ACS DATA')


# if __name__ == "__main__":
#     main()
