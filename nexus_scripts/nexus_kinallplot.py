# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:37:51 2015

Plot Plug-in Gait outputs (online) from Nexus.

@author: Jussi
"""

from gaitutils import Plotter, cfg, register_gui_exception_handler
import logging


def do_plot():

    pl = Plotter()
    pl.open_nexus_trial()
    pl.layout = cfg.layouts.lowerbody_kinall
    maintitleprefix = 'Kinetics/kinematics plot for '

    pl.plot_trial(maintitleprefix=maintitleprefix, show=False)
    pl.move_plot_window(10, 30)
    pl.show()

    if cfg.plot.show_videos:
        for vidfile in pl.trial.video_files:
            pl.external_play_video(vidfile)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    register_gui_exception_handler()
    do_plot()
