# -*- coding: utf-8 -*-
"""

plotting functionality shared between backends

@author: Jussi (jnu@iki.fi)
"""


from builtins import str
from builtins import next
from past.builtins import basestring
from builtins import object
from itertools import cycle
from collections import defaultdict, namedtuple
import datetime
import logging
import copy
import numpy as np

from gaitutils import models, cfg


logger = logging.getLogger(__name__)


def _get_trial_cycles(trial, cycles, max_cycles):
    """Gets the specified cycles from a trial."""
    model_cycles = trial.get_cycles(
        cycles['model'], max_cycles_per_context=max_cycles['model']
    )
    emg_cycles = trial.get_cycles(
        cycles['emg'], max_cycles_per_context=max_cycles['emg']
    )
    allcycles = list(set.union(set(model_cycles), set(emg_cycles)))
    if not allcycles:
        logger.debug('trial %s has no cycles of specified type' % trial.trialname)
    logger.debug(
        'got total of %d cycles for %s (%d model, %d EMG)'
        % (len(allcycles), trial.trialname, len(model_cycles), len(emg_cycles))
    )
    Cyclebunch = namedtuple('Cyclebunch', 'allcycles, model_cycles, emg_cycles')
    return Cyclebunch(allcycles, model_cycles, emg_cycles)


def _emg_yscale(emg_mode):
    """Compute EMG y range for plotting"""
    if emg_mode == 'rms':
        emg_yrange = np.array([0, cfg.plot.emg_yscale]) * cfg.plot.emg_multiplier
    else:
        emg_yrange = (
            np.array([-cfg.plot.emg_yscale, cfg.plot.emg_yscale])
            * cfg.plot.emg_multiplier
        )
    return emg_yrange


def _color_by_params(spec, mapper, trial, cyc, context, dimension=None):
    """Helper to return a color.
    
    spec is colorspec and mapper is a color mapper. Returns color according to
    trial, context etc., depending on what spec says. Depending on spec, color
    may come from the mapper or elsewhere (e.g. config). 'dimension' refers to
    variable dimension in case of multidimensional vars (e.g. markers).
    """
    if spec == 'session':
        return mapper[trial.sessiondir]
    elif spec == 'trial':
        return mapper[trial]
    elif spec == 'cycle':
        return mapper[cyc]
    elif spec == 'context':
        return cfg.plot.context_colors[context]
    elif spec == 'dimension':
        return mapper[dimension]
    elif spec is None:
        return '#000000'
    else:
        raise RuntimeError('Unexpected colorspec: %s' % spec)


def _style_by_params(spec, mapper, trial, cyc, context, dimension=None):
    """Helper to return a style.
    
    See above for details."""
    if spec == 'session':
        return mapper[trial.sessiondir]
    elif spec == 'trial':
        return mapper[trial]
    elif spec == 'cycle':
        return mapper[cyc]
    elif spec == 'context':
        return cfg.plot.context_styles[context]
    elif spec == 'dimension':
        return mapper[dimension]
    elif spec is None:
        return '-'
    else:
        raise RuntimeError('Unexpected colorspec: %s' % spec)


def _cyclical_mapper(it):
    """Map iterator to keys cyclically.

    Example:
    colors = ['red', 'blue', 'yellow']
    mapper = _cyclical_mapper(colors)
    mapper['foo']  # red
    mapper['bar']  # blue
    mapper['baz']  # yellow
    mapper['zzz']  # red (iterator cycles over)
    mapper['foo']  # red (old mappings are preserved)
    """
    cyc_it = cycle(it)
    return defaultdict(lambda: next(cyc_it))


def _handle_cyclespec(cycles):
    """Handle cyclespec argument to plotter functions. """
    default_cycles = cfg.plot.default_cycles
    if cycles == 'unnormalized':
        cycles = {vartype: 'unnormalized' for vartype in default_cycles}
    elif cycles is None:
        cycles = default_cycles
    elif isinstance(cycles, dict):
        if set(cycles) - set(default_cycles):  # unknown keys
            raise ValueError('invalid cycle argument')
        _defcycles = default_cycles.copy()
        _defcycles.update(cycles)
        cycles = _defcycles
    else:
        raise ValueError('invalid cycle argument')
    return cycles


def _handle_style_and_color_args(style_by, color_by):
    """Handle style and color choice"""
    vals_ok = set(('session', 'trial', 'context', 'dimension', None))
    style_by_defaults = cfg.plot.style_by
    if style_by is None:
        style_by = dict()
    elif isinstance(style_by, basestring):
        style_by = {'model': style_by}
    elif not isinstance(style_by, dict):
        raise TypeError('style_by must be str or dict')
    for k in set(style_by_defaults) - set(style_by):
        style_by[k] = style_by_defaults[k]  # update missing values
    if not set(style_by.values()).issubset(vals_ok):
        raise ValueError('invalid style_by argument in %s' % style_by.items())

    color_by_defaults = cfg.plot.color_by
    if color_by is None:
        color_by = dict()
    elif isinstance(color_by, basestring):
        color_by = {'model': color_by, 'emg': color_by}
    elif not isinstance(color_by, dict):
        raise TypeError('color_by must be str or dict')
    for k in set(color_by_defaults) - set(color_by):
        color_by[k] = color_by_defaults[k]  # update missing values
    if not set(color_by.values()).issubset(vals_ok):
        raise ValueError('invalid color_by argument in %s' % color_by.items())

    return style_by, color_by


def _style_mpl_to_plotly(style):
    """Style mapper matplotlib -> plotly"""
    return {'-': 'solid', '--': '5px', '-.': 'dashdot', '..': '2px'}[style]


def _var_title(var):
    """Get proper title for variable"""
    mod = models.model_from_var(var)
    if mod:
        if var in mod.varlabels_noside:
            return mod.varlabels_noside[var]
        elif var in mod.varlabels:
            return mod.varlabels[var]
    elif var in cfg.emg.channel_labels:
        return cfg.emg.channel_labels[var]
    else:
        return var


def _truncate_trialname(trialname):
    """Shorten trial name."""
    try:
        # try to truncate date string of the form yyyy_mm_dd
        tn_split = trialname.split('_')
        datetxt = '-'.join(tn_split[:3])
        d = datetime.datetime.strptime(datetxt, '%Y-%m-%d')
        return '%d..%s' % (d.year, '_'.join(tn_split[3:]))
    except ValueError:  # trial was not named as expected
        return trialname


def _get_cycle_name(trial, cyc, name_type):
    """Return descriptive name for a gait cycle"""
    if name_type == 'name_with_tag':
        cyclename = '%s / %s' % (trial.trialname, trial.eclipse_tag)
    elif name_type == 'short_name_with_tag':
        cyclename = '%s / %s' % (
            _truncate_trialname(trial.trialname),
            trial.eclipse_tag,
        )
    elif name_type == 'short_name_with_tag_and_cycle':
        cyclename = _truncate_trialname(trial.trialname)
        if trial.eclipse_tag is not None:
            cyclename += ' (%s)' % trial.eclipse_tag
        cyclename += ' / '
        cyclename += cyc.name
    elif name_type == 'tag_only':
        cyclename = trial.eclipse_tag
    elif name_type == 'tag_with_cycle':
        cyclename = '%s / %s' % (trial.eclipse_tag, cyc.name)
    elif name_type == 'full':
        cyclename = '%s / %s' % (trial.name_with_description, cyc.name)
    elif name_type == 'short_name_with_cyclename':
        cyclename = '%s / %s' % (_truncate_trialname(trial.trialname), cyc.name)
    else:
        raise ValueError('Invalid name_type')
    return cyclename
