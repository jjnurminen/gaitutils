# -*- coding: utf-8 -*-
"""

Test EMG functions.

@author: Jussi (jnu@iki.fi)
"""

import pytest
import logging
import tempfile
import os.path as op

from gaitutils import sessionutils, emg, GaitDataError
from utils import _file_path

logger = logging.getLogger(__name__)


# test session
sessiondir_ = 'test_subjects/D0063_RR/2018_12_17_preOp_RR'
sessiondir_abs = _file_path(sessiondir_)
sessiondir2_ = 'test_subjects/D0063_RR/2018_12_17_preOp_tuet_RR'
sessiondir2_abs = _file_path(sessiondir2_)
sessiondir__ = op.split(sessiondir_)[-1]
sessions = [sessiondir_abs, sessiondir2_abs]
tmpdir = tempfile.gettempdir()


def test_emg_detect_bads():
    """Test bad channel detection"""
    # this file is tricky; RVas is disconnected but shows some kind of artifact
    fn = r'2018_12_17_preOp_RR21.c3d'
    fpath = op.join(sessiondir_abs, fn)
    e = emg.EMG(fpath)
    expected_ok = {
        'RGas': True,
        'LHam': True,
        'RSol': True,
        'RGlut': False,
        'LVas': False,
        'LGas': True,
        'LRec': True,
        'RPer': True,
        'RVas': False,
        'LSol': True,
        'RTibA': True,
        'RHam': True,
        'LTibA': True,
        'RRec': True,
        'LPer': True,
        'LGlut': False,
    }
    for chname, exp_ok in expected_ok.items():
        assert e.status_ok(chname) == exp_ok




