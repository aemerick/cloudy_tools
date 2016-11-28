import numpy as np
import matplotlib.pyplot as plt
import h5py

outtype = 'heating'

nrow = 5
ncol = 6

nz = 25

dz = nz

metals = False

if metals:
    nosh_dir = 'hm_2011_nosh_metals/'
    cr_dir   = 'hm_2011_sh_final_CR/'
    ncr_dir  = 'hm_2011_sh_final/'
    combined_dir = 'hm_2011_shield_combined/'
else:
    nosh_dir = 'hm_2011_nosh/'
    cr_dir   = 'hm_2011_sh_final_mf_CR/'
    ncr_dir  = 'hm_2011_sh_final_mf/'
    combined_dir = 'hm_2011_shield_combined_mf_fixed/'


hdens = np.arange(-10, 4.5, 0.5)

if outtype == 'cooling':
    field = 'Cooling'
else:
    field = 'Heating'



hf = h5py.File('/home/emerick/code/grackle/input/CloudyData_UVB=HM2012.h5','r')
pcool = hf['CoolingRates/Primordial/' + field]
mcool = hf['CoolingRates/Metals/' + field]

for zi in np.arange(1, nz+1):

    print zi
    fig, ax = plt.subplots(nrow,ncol)
    fig.set_size_inches(4*ncol,4*nrow)

    row = 0; col = 0
    for index in np.arange(np.size(hdens)):
        i = zi + dz*index

        try:
            cr_data  = np.genfromtxt(cr_dir + 'hm_2011_sh_run%i.dat'%(i), skip_header = 14, names = True)
            ax[(row,col)].plot(cr_data['Te'], cr_data[field], label = 'CR', lw = 3, ls = '--', color = 'black')
        except:
            print cr_dir + 'cosmic ray data does not exist'

        ncr_data = np.genfromtxt(ncr_dir + 'hm_2011_sh_run%i.dat'%(i), skip_header = 14, names=True)
        combined_data = np.genfromtxt(combined_dir + 'hm_2011_sh_run%i.dat'%(i), names=True)

        try:
            nosh_data = np.genfromtxt(nosh_dir + 'hm_2011_run%i.dat'%(i), skip_header = 14, names = True)
            ax[(row,col)].plot(nosh_data['Te'], nosh_data[field], label = 'No Shield', lw = 3, ls = '--', color = 'blue')
        except:
            print nosh_dir + 'hm_2011_run%i.dat does not exist'%(i)

        ax[(row,col)].plot(ncr_data['Te'], ncr_data[field], label = "No CR", lw = 3, ls = '-', color ='black')

        ax[(row,col)].plot(combined_data['Te'], combined_data[field], label = 'combined', lw = 3, color = 'red', ls = ':')

        if not metals:
            ax[(row,col)].plot(combined_data['Te'], pcool[index][zi], label = 'cloudy', lw = 3, color = 'purple', ls ='--')

        ax[(row,col)].loglog()
        ax[(row,col)].set_xlabel(r'Temperature (K)')
        if field == 'cooling':
            label = r'Cooling Rate (erg s$^{-1}$ cm$^{-3}$)'
        else:
            label = r'Heating Rate (erg s$^{-1}$ cm$^{-3}$)'

        ax[(row,col)].set_ylabel(label)

        if index == 0:
            ax[(row,col)].legend(loc='best')
        ax[(row,col)].set_title(r'log(n$_{\rm{H}}$) = %.2f'%(hdens[index]))

        col = col + 1
        if col >=ncol:
            col = 0
            row = row + 1

    plt.tight_layout()

    if metals:
        fig.savefig('./plots/metals/' + outtype + 'z%i.png'%(zi))
    else:
        fig.savefig('./plots/mf/' + outtype + 'z%i.png'%(zi))
    plt.close()
