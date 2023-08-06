# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QFileDialog)

from errorcalcsbeta import ecfuncs
from errorcalcsbeta import main_window


class File():
    def new():
        pass

    def _open_():
        pass

    def save():
        datei_inputs = open('.__log__/inputs.txt', 'w')

        variable = ecfuncs.inputs.variable_list
        value = ecfuncs.inputs.value_list
        error = ecfuncs.inputs.error_list

        if len(variable) == len(value):
            length = len(variable)
            for v in range(length):
                if variable[v] == '':
                    pass
                else:
                    print(variable[v].replace(' ', ''), value[v], error[v],
                          file=datei_inputs)
        else:
            pass
        datei_inputs.close()

    def exportFormulaNew():
        formula = ecfuncs.inputs.formula_list
        here = main_window.main_Widget.file_Dialog()
        to_export = ecfuncs.file_options.export_line()
        print('{}\n{}'.format(formula[-1], to_export[1]), file=here)

    def exportFormulaAppend():
        pass

    def quitMain():
        pass

    def restartMain():
        pass


class View():
    def fullScreen():
        pass


class Help():
    def usage():
        pass

    def shortcut():
        pass

    def update():
        pass


class Ec():
    def donate():
        pass

    def git():
        pass

    def web():
        pass

    def pypi():
        pass
