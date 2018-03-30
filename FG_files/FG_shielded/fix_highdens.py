import numpy as np

run_min = 1
run_max = 639
nz      = 22

#
# In generating the metal free data, I needed to pull the non-cr
# runs for high density since the CR runs were not used for metals at these densities
# This was needed in order to properly subtract out from the metal data set to get
# the metal only contribution. But this should be the same regardless of the shielding.
# Therefore, go back to the correct full shielding run data for the high densities
# where we only temporarily used the less-than-full-jeans-length non-CR runs
#
#

def run_on_all_data(data_dir, cr_dir, output_dir, data_name = None, cr_data_name = None,hdens = 2.5):

    if data_name is None:
        data_name = data_dir
    if cr_data_name is None:
        cr_data_name = cr_dir

    runs = np.arange(run_min, run_max)

    densities = (np.array([np.arange(-10, 4.5, 0.5)]*nz).transpose()).flatten()



    id = 0
    iz = 0

    for i in runs:
        data = np.genfromtxt(data_dir + '/' + data_name + '_run%i.dat'%(i), names = True)

        if densities[i-1] >= hdens:

            crdata = np.genfromtxt(cr_dir + '/' + cr_data_name + '_run%i.dat'%(i), names = True, skip_header = 14)

            selection = crdata['Cooling'] < data['Cooling'][:np.size(crdata['Cooling'])]

            data['Cooling'][:np.size(crdata['Cooling'])][selection] = crdata['Cooling'][selection]
            data['Heating'][:np.size(crdata['Cooling'])][selection] = crdata['Heating'][selection]

        np.savetxt(output_dir + '/' + data_name + '_run%i.dat'%(i), data, fmt='%.6E', header = "Te Heating Cooling MMW")


        iz = iz + 1
        if iz >= 25:
            iz = 0
            id = id + 1

    return

if __name__ == '__main__':

#    run_on_all_data('hm_2011_shield_combined_mf', 'hm_2011_sh_final_mf_CR', 'hm_2011_sh',
#                     'hm_2011_shield_combined_mf_fixed')

    run_on_all_data('fg_2011_shield_combined_mf', 'fg_2011_sh_cr_mf', 'fg_2011_shield_combined_mf_fixed')
