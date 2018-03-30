import numpy as np
from scipy.interpolate import interp1d

rmin = 1
rmax = 639

def fill_in_gaps(x, y):
    #
    # find the negative values
    #
    y = y * 1.0

    if y[0] <= 0.0:
        y[0]  = y[ y > 0.0][0]

    if y[-1] <= 0.0:
        y[-1] = y[ y > 0.0][-1]

    x_pos = x[ y >  0.0]
    x_neg = x[ y <= 0.0]

    if np.size(x_neg) < 1:
        return y

    f = interp1d(x_pos, y[y > 0.0], kind = 'linear')

    y[ y <= 0.0] = f(x_neg)


    return y

def run_on_all_data(data_dir, data_name, output_dir):

    runs = np.arange(rmin, rmax ,1)

    for i in runs:
        data = np.genfromtxt(data_dir + '/' + data_name + '_run%i.dat'%(i), names = True)

        old_heating = data['Heating'] * 1.0

        data['Cooling'] = fill_in_gaps(data['Te'], data['Cooling']*1.0)
        data['Heating'] = fill_in_gaps(data['Te'], data['Heating']*1.0)

        np.savetxt(output_dir + '/' + data_name + '_run%i.dat'%(i), data, fmt='%.6E', header = "Te Heating Cooling MMW")

        output = 'run %i'%(i)

        if (any(old_heating <= 0.0)):
            output += ' contained negative values'
        else:
            output += ' had no negative values'

        if (any(data['Heating'] <=0.0) and any(old_heating <=0.0)):
            output += ' and is STILL NEGATIVE'
        else:
            output += ' and has no negative values'

        print output

    return


if __name__ == '__main__':
#    run_on_all_data('subtracted_cooling_final', 'hm_2011_shield_metal_only', 'filled_in_subtracted_final')
    run_on_all_data('fg_2011_shield_metal_only', 'fg_2011_shield_metal_only', 'fg_2011_filled_in_metal_only')





