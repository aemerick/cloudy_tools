import numpy as np
import matplotlib.pyplot as plt
import h5py

outtype = 'cooling'

nrow = 5
ncol = 6

nz = 25

dz = nz

metal_only = True

hdens = np.arange(-10, 4.5, 0.5)


hf = h5py.File('/home/emerick/code/grackle/input/CloudyData_UVB=HM2012.h5','r')
pcool = hf['CoolingRates/Primordial/Cooling']
mcool = hf['CoolingRates/Metals/Cooling']

monly_dir = './filled_in_subtracted_final/'
msmooth_dir = './smoothing/'

for zi in np.arange(1, nz+1):

    print zi
    fig, ax = plt.subplots(nrow,ncol)
    fig.set_size_inches(4*ncol,4*nrow)

    row = 0; col = 0
    output = ""
    for index in np.arange(np.size(hdens)):
        i = zi + dz*index

        output += " run %i"%(i)

        metal_only = np.genfromtxt(monly_dir + '/hm_2011_shield_metal_only_run%i.dat'%(i),names=True)
        metal_smooth = np.genfromtxt(msmooth_dir + '/hm_2011_shield_metal_only_run%i.dat'%(i), names=True)
        ax[(row,col)].plot(metal_only['Te'], metal_only['Cooling'] * 1.0E3, label = "Shield x 1000", lw = 3, ls = '-', color ='black')
        ax[(row,col)].plot(metal_smooth['Te'], metal_smooth['Cooling'] *1.0E3, label = 'smooth', lw = 3 , ls = '--', color = 'green')

        ax[(row,col)].plot(metal_only['Te'], mcool[index][zi], label = 'Cloudy', lw = 3, color = 'red', ls = ':')


        ax[(row,col)].loglog()
        ax[(row,col)].set_xlabel(r'Temperature (K)')
        ax[(row,col)].set_ylabel(r'Coolinrg Rate (erg s$^{-1}$ cm$^{-3}$)')

        if index == 0:
            ax[(row,col)].legend(loc='best')
        ax[(row,col)].set_title(r'log(n$_{\rm{H}}$) = %.2f'%(hdens[index]))

        col = col + 1
        if col >=ncol:
            col = 0
            row = row + 1

    print output

    plt.tight_layout()

    fig.savefig('./plots/metal_only/' + outtype + 'z%i.png'%(zi))
    plt.close()
