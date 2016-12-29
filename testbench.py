# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 14:06:22 2016

Test new gaitutils code

@author: HUS20664877
"""

from gaitutils import EMG, nexus, config, read_data, trial, eclipse, models, Plotter, layouts, utils
import matplotlib.pyplot as plt


# c3dfile = u'c:\\Users\\hus20664877\\Desktop\\Vicon\\vicon_data\\test\\H0036_EV\\2015_9_21_seur_EV\\2015_9_21_seur_EV19.c3d'
vicon = nexus.viconnexus()


lout = [['LVas', 'RVas'], ['LRec', 'RRec'], ['LHam', 'RHam']]
lout = layouts.kinetics_emg('R')



# online kinematics plot
lout = [['PelvisAnglesX', 'PelvisAnglesY', 'PelvisAnglesZ'],
        ['HipAnglesX', 'HipAnglesY', 'HipAnglesZ'],
        ['KneeAnglesX', 'KneeAnglesY', 'KneeAnglesZ'],
        ['AnkleAnglesX', 'FootProgressAnglesZ', 'AnkleAnglesZ']]


def layout_with_sides(lout):
    """ Helper to create superposed layouts (superpose L/R) from layouts
    where side is not specified """
    newlout = []
    for row in lout:
        newrow = []
        for var in row:
            if var is not None and var[0] not in ['L', 'R']:
                newrow.append(['L'+var, 'R'+var])
            else:
                newrow.append(var)
        newlout.append(newrow)
    return newlout


def get_layout_context(lout):
    context = []
    for row in lout:
        newrow = []
        for var in row:
            if isinstance(var, list):
                varli = []
                for var_ in var:
                    if var_ is not None and var_[0] in ['L', 'R']:
                        varli.append(var_[0])
                    else:
                        varli.append(None)
                newrow.append(varli)
            elif var is not None and var[0] in ['L', 'R']:
                newrow.append(var[0])
            else:
                newrow.append(None)
        context.append(newrow)
    return context


l2 = layout_with_sides(lout)


pl = Plotter()

pl.layout = l2

pl.open_nexus_trial()

#pl.plot_trial()

pl.plot_trial(model_cycles={'R':1, 'L':1})






