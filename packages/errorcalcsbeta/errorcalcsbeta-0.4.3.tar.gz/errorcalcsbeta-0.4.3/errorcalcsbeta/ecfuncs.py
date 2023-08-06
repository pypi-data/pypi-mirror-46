# -*- coding: utf-8 -*-
"""
CalcS
ecfuncs for main_window buttons etc.
"""
import main_window
import uncertainties as uc
from uncertainties.umath import *
from PyQt5.QtWidgets import (QFileDialog)


class button_Funcs():
    def addVar(var, val, err):
        inputs.variable_list.append(var)
        inputs.value_list.append(val)
        inputs.error_list.append(err)

    def variableFunc():
        variable = inputs.variable_list
        value = inputs.value_list
        error = inputs.error_list

        if str(error[-1]) == '':
            i = '{} = {} +/- 0'.format(variable[-1], value[-1])
            inputs.error_list.append('0')
        else:
            i = '{} = {} +/- {}'.format(variable[-1], value[-1], error[-1])

        return i

    def calculate(formula):
        variable = inputs.variable_list
        value = inputs.value_list
        error = inputs.error_list

        result = calc.errorcalc(variable, value, error, formula)

        way = '{} = {}'.format(formula, result)
        inputs.way_list.append(way)

        return inputs.way_list, result

class calc():
    def build_var(n, v):
        globals()[n] = v

    def part_abl(v, f):
        from sympy import diff, sympify

        try:
            f = sympify(f)
            return [str(f.diff(i)) for i in v]
        except TypeError:
            return ['error']

    def errorcalc(variable, value, error, formula):        
        if len(variable) == len(value):
            length = len(variable)
            for v in range(length):
                calc.build_var(variable[v], uc.ufloat_fromstr(value[v], error[v]))
            try:
                _result_ = eval(formula)
                result = '{:.5u}'.format(_result_)
            except:
                result = 'error'
        return result


class inputs():
    variable_list = []
    value_list = []
    error_list = []

    formula_list = []

    way_list = []

    part_abl = []


class file_options():

    def check_empty(_file_):
        f = open(_file_, 'r')
        empty = True
        for line in f:
            if line:
                empty = False
        
        return empty

    def export_line():
        var = inputs.var
        formula = inputs.formula_list[-1]
        part_de = calc.part_abl(var, formula)
        gauss = ('\Delta_{s}=\sqrt{(\\frac{\partial s}{\partial x})^{2}*(dx)' +
                 '^{2}+(\\frac{\partial s}{\partial y})^{2}*(dy)^{2}}')
        x = ''
        for i in range(len(part_de)):
            x += '({})^{{2}}*(d{})^{{2}}'.format(
                                            str(part_de[i]).replace('**', '*'),
                                            str(var[i]).replace('**', '^')
                                            )
            if i < len(part_de):
                x += '+'
        
        return gauss, '∆s = sqrt({})\n'.format(x)