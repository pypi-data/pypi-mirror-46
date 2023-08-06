"""Signal processing module
"""
from scipy.signal import butter, filtfilt

def low_pass(sig, time, freq_cutoff, N=5):
    """Applies a Nth order butterworth lowpass filter.
    
    Parameters
    ----------
    sig : list
        Signal to be filtered
    time : list
        Time signal associated with `sig`
    freq_cutoff : int
        Cutoff frequency to use when filtering
    N : int
        Order of butterworth filter (default is 5)
    
    Returns
    -------
    list
        Filtered signal
    list
        Time signal associated with filtered signal

    """
    freq_samp = 1/(time[1]-time[0])
    omega = freq_cutoff/freq_samp*2
    b_coef, a_coef = butter(N, omega)
    return list(filtfilt(b_coef, a_coef, sig)), time
        
def step_function(index, start, init_val, end, final_val):
    """Approximates the Heaviside step function with a cubic polynomial.
    
    Example
    -------
    >>> x = [2, 3, 3.5, 4, 5]
    >>> start = 3
    >>> init_val = 0
    >>> end = 3
    >>> final_val = 1
    >>> step_function(x, start, init_val, end, final_val)
    [0.0, 0.0, 0.5, 1.0, 1.0]
    
    Parameters
    ----------
    index : list
        Independent variable
    start : float
        Value of independent variable at which the STEP function begins
    init_val : float
        Initial value of the step
    end : float
        Value of independent variable at which the STEP function ends
    final_val : float
        Final value of the step
    
    Returns
    -------
    list
        Resulting step function
    """

    height = final_val - init_val
    step =  [init_val for ind in index if ind <= start]    
    step += [init_val + height*((ind-start)/(end-start))**2 * (3-2*((ind-start)/(end-start))) for ind in index if start < ind < end]
    step += [final_val for ind in index if ind >= end]
    return step
