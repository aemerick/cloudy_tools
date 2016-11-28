import numpy as np
import matplotlib.pyplot as plt
import h5py

outtype = 'heating'

nrow = 5
ncol = 6

nz = 26

dz = nz

metals = False

hdens = np.arange(-10, 4.5, 0.5)

if outtype == 'cooling':
    field = 'Cooling'
else:
    field = 'Heating'

hf = h5py.File('/home/emerick/code/grackle/input/CloudyData_UVB=HM2012.h5','r')
pcool = hf['CoolingRates/Primordial/' + field]
mcool = hf['CoolingRates/Metals/' + field]

newhf = h5py.File('./new_table.h5','r')
npcool =newhf['CoolingRates/Primordial/' + field]
nmcool = newhf['CoolingRates/Metals/' + field]

Te = np.logspace(1., 9., 161)


if metals:
    old_data = mcool
    new_data = nmcool
else:
    old_data = pcool
    new_data = npcool

for zi in np.arange(1, nz+1):

    print zi
    fig, ax = plt.subplots(nrow,ncol)
    fig.set_size_inches(4*ncol,4*nrow)

    row = 0; col = 0
    for index in np.arange(np.size(hdens)):

        ax[(row,col)].plot(Te, old_data[index][zi], label = 'old data', lw = 3, color = 'red', ls ='--')
        ax[(row,col)].plot(Te, new_data[index][zi], label = 'new data', lw = 3, color = 'black', ls = '-')

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
        fig.savefig('./plots/final/metals/' + outtype + 'z%i.png'%(zi))
    else:
        fig.savefig('./plots/final/mf/' + outtype + 'z%i.png'%(zi))
    plt.close()
