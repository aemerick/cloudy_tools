import numpy as np

def simple_smooth(x, y, window = 1, interp = 1, factor = 3.0, interpolation = 'linear', mode = 'spike'):
    """
    Very simple smoothing method meant to best handle data with occasional single spiked
    points, where the "spike" is defined as being a factor "factor" larger than the points
    on either side. Linear interpolation is used to smooth out these bad points.

    For example, if window = 1 and interp = 1, iterates through every point, checking if
    y[i]/y[i-1] and y[i]/y[i+1] are both greater than factor. If so, interpolates between
    y[i-1] and y[i+1] to fill this value. If window = 2 and interp = 1, looks at
    y[i]/y[i-2] and y[i]/y[i+2] instead, with same interpolation. In general:

    window size sets:   y[i]/y[i-window] and y[i]/y[i+window] test values
    and interp sets the points to interpolate between (y[i+interp] and y[i-interp].

    Suggested use is to run once with window = 1 and interp = 1 (default) and a second time
    with window = 2 and interp = 1
    """


    if interp > window:
        raise ValueError("Interpolation size must be less than or equal to window size")

    smooth_y = 1.0 * y

    # iterate through y, picking out spikes and smoothing them
    # define a spike as a point where difference on either side is
    # an order of magnitude or more

    if mode == 'spike':

        for i in np.arange(window, np.size(y) - window):

            if (( (y[i] / smooth_y[i - window]) > factor) and ((y[i]/y[i+window]) > factor)):
                smooth_y[i] =  (((y[i+interp] - y[i-interp]) / (x[i+interp] - x[i-interp]))) * (x[i] - x[i-interp]) + y[i-interp]

    else:
        # loop through again, taking care of dips
        for i in np.arange(window, np.size(y) - window):
            if (( (y[i] / smooth_y[i-window]) < factor) and ((y[i]/y[i+window]) < factor)):
                smooth_y[i] = (((y[i+interp] - y[i-interp]) / (x[i+interp] - x[i-interp])))*(x[i] - x[i-interp]) + y[i-interp]

    return smooth_y

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    import numpy as np
    from math import factorial
    
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')


def run_on_all_data(data_dir, data_name, output_dir, iterations = 1):
    runs = np.arange(1, 726)

    for i in runs:
        data = np.genfromtxt(data_dir + '/' + data_name + '_run%i.dat'%(i), names = True)
        old_heating = data['Heating'] * 1.0

        for n in np.arange(iterations):
#            data['Cooling'] = 10.0**(savitzky_golay(np.log10(data['Cooling']*1000.0), 37, 4)) / 1000.0

            data['Heating'] = 10.0**(savitzky_golay(np.log10(data['Heating']*1000.0),
                                                    37, 4)) / 1000.0

        data['Cooling'] = simple_smooth(data['Te'], data['Cooling']*1000.0 ) / 1000.0
        data['Cooling'] = simple_smooth(data['Te'], data['Cooling']*1000.0, window = 2, interp = 2 ) / 1000.0
        data['Cooling'] = simple_smooth(data['Te'], data['Cooling']*1000.0, factor = 5.0, window = 3, interp = 3 ) / 1000.0
        data['Cooling'] = simple_smooth(data['Te'], data['Cooling']*1000.0, window = 1, interp = 1 ) / 1000.0


        # now deal with dips
        data['Cooling'] = simple_smooth(data['Te'], data['Cooling']*1000.0, window = 1, interp = 1, mode = 'dip') / 1000.0

        np.savetxt(output_dir + '/' + data_name + '_run%i.dat'%(i), data, fmt='%.6E', header = "Te Heating Cooling MMW")

        print 'run %i'%(i)

    return



#
# n = 7 or 11 works for number of iterations
#
# 31 works for window size
#  4 works for poly
#

if __name__ == '__main__':

    n = 11

    run_on_all_data('filled_in_subtracted_final', 'hm_2011_shield_metal_only',
                     'smoothing', iterations = n )
