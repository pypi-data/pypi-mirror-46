"""
Author: Diego Pinheiro
github: https://github.com/diegompin

"""

from acs_wrapper.src.parameters import Parameter
from acs_wrapper.src.util_multiprocessing import MyPool


class ScriptBase(object):
    PAR_SCRIPT_NAME = 'script.name'
    PAR_SCRIPT_PROCESSES = 'script.processes'
    PAR_SCRIPT_DATA_LINK_OUTPUT = 'script.data_link_output'
    PAR_SCRIPT_DATA_LINK_INPUT = 'script.data_link_input'
    PAR_SCRIPT_FILE_FORMAT = 'script.plot_format'


    def __init__(self, par):
        self.pool = MyPool
        self.par = par
        self.name = Parameter.get_par(par, ScriptBase.PAR_SCRIPT_NAME, 'unnamed')
        self.data_link_input = Parameter.get_par(par, ScriptBase.PAR_SCRIPT_DATA_LINK_INPUT, '.')
        self.data_link_output = Parameter.get_par(par, ScriptBase.PAR_SCRIPT_DATA_LINK_OUTPUT, '.')
        self.params = self.get_params()
        self.processes = Parameter.get_par(par, ScriptBase.PAR_SCRIPT_PROCESSES, 4)
        self.file_format = Parameter.get_par(par, ScriptBase.PAR_SCRIPT_FILE_FORMAT, 'PDF')

    def map(self, func, params):
        with self.pool(processes=self.processes) as pool:
            pool.map(func, params)

    def get_params(self):
        pass

    def get_func(self, params):
        pass
        # data_link_output = self.data_link_output
        # filename = self.get_filename(params)
        # file_output = '%s/%s.pdf' % (data_link_output, filename)
        # print(file_output)

    def get_file_output(self, params):
        pass

    def main(self, *args):
        self.params = self.get_params()
        print('INITIALIZING SCRIPT...')
        # for arg in args:
        #     k = arg.split("=")[0]
        #     v = arg.split("=")[1]
        #     self.par[k] = v
        #     print(f"Argument: {k} = {v}")
        self.map(self.get_func, self.params)
        # self.script()
        print('SCRIPT FINISHED!')

    # def get_filename(self, params):
    #     filename = self.name
    #     for par in params:
    #         # if isinstance(par, str):
    #         if isinstance(par, pd.DataFrame):
    #             filename += '__%s__' % par.name
    #         else:
    #             filename += '__%s__' % par
    #     return filename

