# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the PyMVPA package for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Helper to print pretty progress indicator.

"""

__docformat__ = 'restructuredtext'

import time
import datetime
import math

def seconds2prettystring(t, ndigits=0):
    '''Prints seconds in a pretty form
    
    Parameters
    ----------
    t: float
        time in seconds
        
    Returns
    s: str
        time represented as a string HH:MM:SS
        
    '''
    if t < 0:
        return '-' + seconds2prettystring(-t, ndigits)

    if t == t + 1.:
        return 'oo' # infinity

    seconds_per_day = 60 * 60 * 24
    ndays = int(t) / seconds_per_day
    nseconds = t - ndays * seconds_per_day
    sec_str = str(datetime.timedelta(seconds=nseconds))

    # split on decimal point
    sec_split = sec_str.split('.')

    if len(sec_split) != 1:
        big, small = sec_split # before and after dot
        if ndigits == 0:
            sec_str = big
        else:
            sec_str = '%s.%s' % (big, small[:min(len(small), ndigits)])

    return sec_str if ndays == 0 else '%dd:%s' % (ndays, sec_str)


def eta_string(start_time, progress, msg=None,
                progress_bar_width=18, show_percentage=True):
    '''Simple linear extrapolation to estimate how much time is needed 
    to complete a task.
    
    Parameters
    ----------
    starttime
        Time the tqsk started, from 'time.time()'
    progress: float
        Between 0 (nothing completed) and 1 (fully completed)
    msg: str (optional)
        Message that describes progress - is added to the output
    progress_bar_width: int (default: 18)
        Width of progress bar. If zero then no progress bar is shown.
    show_percentage: bool (default: True)
        Show progress in percentage?
        
    Returns
    -------
    eta
        Estimated time until completion formatter pretty, 
    
    Notes
    -----
    ETA refers to "estimated time of arrival".
    '''
    SYM_DONE = '='
    SYM_TODO = '_'

    now = time.time()
    took = now - start_time

    legal_progress = 0 < progress <= 1
    eta = took * (1 - progress) / progress if legal_progress \
                                           else progress * float('inf')
    pct_str = '[%.0f%%]' % (progress * 100.)

    swap_sign = lambda x:'+' + x[1:] if len(x) > 0 and x[0] == '-' else '-' + x

    formatter = seconds2prettystring


    if progress_bar_width:
        n_done = int(math.floor(min(progress, 1.) * progress_bar_width))
        n_todo = progress_bar_width - n_done

        done = SYM_DONE * n_done
        todo = SYM_TODO * n_todo

        if show_percentage:
            n_pct = len(pct_str)
            margin = 2
            n = n_pct + margin # required length for pct string
            if n <= n_done and (n > n_todo or n_done >= n_todo):
                offset = (n_done - margin - n_pct / 2) / 2

                done = done[:offset] + pct_str + \
                        done[:(n_done - offset - n_pct)]
            elif n <= n_todo:
                offset = (n_todo - (n_pct + margin) / 2) / 2
                todo = todo[:offset] + pct_str + \
                        todo[:(n_todo - offset - n_pct)]


        bar = done + todo
    else:
        bar = pct_str

    full_msg = '+%s %s %s' % (formatter(took), bar,
                                swap_sign(formatter(eta)))
    if not msg is None:
        full_msg = '%s  %s' % (full_msg, msg)
    return full_msg

