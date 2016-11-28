import numpy as np


runs = np.arange(1,726,1)


for i in runs:
    print i
    metals = np.genfromtxt('hm_2011_shield_combined/hm_2011_sh_run%i.dat'%(i), names = True)
    mf     = np.genfromtxt('hm_2011_shield_combined_mf/hm_2011_sh_run%i.dat'%(i), names = True)

    subtracted = metals

    subtracted['Cooling']  = metals['Cooling'] -  mf['Cooling']
    subtracted['Heating']  = metals['Heating'] -  mf['Heating']

    np.savetxt('subtracted_cooling_final/hm_2011_shield_metal_only_run%i.dat'%(i), subtracted, fmt='%.6E', header = "Te Heating Cooling MMW")


