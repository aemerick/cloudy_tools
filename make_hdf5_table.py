import numpy as np
import h5py as h5

#
#
# Final data directories:
#
# Note, metal only tables need to be scaled up by 1000 first
#
# Metal Only: /smoothing/
# Metal Free: /hm_2011_shield_combined_mf_fixed/
#
#
#



def construct_table(metal_dir, metal_name,
                    mf_dir, mf_name, original_table,
                    out_table = 'new_table.h5',
                    optically_thin_heating = False):

    new_table = h5.File(out_table, 'w')

    # copy over everything
    original_table.copy('CoolingRates', new_table)
    original_table.copy('UVBRates', new_table)

    # generate new data sets
    mf_cooling = set_up_dataset(mf_dir, mf_name, original_table['CoolingRates/Primordial'], 'Cooling')
    mf_heating = set_up_dataset(mf_dir, mf_name, original_table['CoolingRates/Primordial'], 'Heating')
    mf_MMW     = set_up_dataset(mf_dir, mf_name, original_table['CoolingRates/Primordial'], 'MMW')

    metal_cooling = set_up_dataset(metal_dir, metal_name, original_table['CoolingRates/Metals'], 'Cooling', metals = True)
    metal_heating = set_up_dataset(metal_dir, metal_name, original_table['CoolingRates/Metals'], 'Heating', metals = True)

    # overwrite old data sets
    new_table['CoolingRates/Primordial/Cooling'][...] = mf_cooling
    new_table['CoolingRates/Primordial/MMW'][...]     = mf_MMW

    new_table['CoolingRates/Metals/Cooling'][...] = metal_cooling

    if not optically_thin_heating:
        new_table['CoolingRates/Primordial/Heating'][...] = mf_heating
        new_table['CoolingRates/Metals/Heating'][...] = metal_heating

    new_table.close()

    return


def set_up_dataset(fdir, runname, olddata, name = 'Cooling', data_shape = (29, 26, 161), metals=False):

    idens = 0
    iz    = 0

    data  = np.zeros(data_shape)

    cdata = olddata[name]

    factor = 1.0
    if metals:
        factor = 1000.0

    i = 1
    while i < 726:
#   for i in np.arange(1, 726, 1):

        if iz == 25:
            # just use old cloudy data
            data[idens][iz,:] = cdata[idens][iz,:]

        else:

            new_data = np.genfromtxt(fdir + runname + '_run%i.dat'%(i), names = True)

            data[idens][iz,:] = new_data[name] * factor
            i = i + 1

        # iterate counters
        iz = iz + 1
        if iz >= 26:
            iz = 0
            idens = idens + 1


    return data


if __name__ == '__main__':

    metal_only_dir = '/home/emerick/work/cloudy_tables/HM_2011/smoothing/'
    metal_only_name = 'hm_2011_shield_metal_only'
    mf_dir         = '/home/emerick/work/cloudy_tables/HM_2011/hm_2011_shield_combined_mf_fixed/'
    mf_name        = 'hm_2011_sh'

    original_table = h5.File('/home/emerick/code/grackle-emerick/input/CloudyData_UVB=HM2012.h5','r')

    construct_table(metal_only_dir, metal_only_name, mf_dir, mf_name, original_table,
                    out_table = 'CloudyData_UVB=HM2012_shielded.h5')

    construct_table(metal_only_dir, metal_only_name, mf_dir, mf_name, original_table,
                    out_table = 'CloudyData_UVB=HM2012_shielded_cooling_only.h5',
                    optically_thin_heating = True)

    original_table.close()
