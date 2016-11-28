import numpy as np
import h5py

def run_on_all_data(data_dir, data_name, output_dir, lowdens = -7.5):
    runs = np.arange(1, 726)

    hdens = (np.array([np.arange(-10, 4.5, 0.5)]*25).transpose()).flatten()

    hf = h5py.File('/home/emerick/code/grackle/input/CloudyData_UVB=HM2012.h5','r')
    cloudy_cool = hf['CoolingRates/Metals/Cooling']


    id = 0
    iz = 0

    for i in runs:

        if hdens[i-1] <= lowdens:
            data = np.genfromtxt(data_dir + '/' + data_name + '_run%i.dat'%(i), names = True)

            cloudy_vals = cloudy_cool[id][iz,:]
            cooling     = data['Cooling'] * 1000.0

            cooling[ cooling < cloudy_vals] = cloudy_vals[cooling < cloudy_vals]

            data['Cooling'] = cooling / 1000.0

            np.savetxt(output_dir + '/' + data_name + '_run%i.dat'%(i), data, fmt='%.6E', header = "Te Heating Cooling MMW")

        iz = iz + 1
        if iz >= 25:
            iz = 0
            id = id + 1

    return

if __name__ == '__main__':

    run_on_all_data('smoothing', 'hm_2011_shield_metal_only',
                     'smoothing')
