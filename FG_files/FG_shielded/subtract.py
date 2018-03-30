import numpy as np

rmin = 1
rmax = 639
nz   = 22


#metal_name = 'hm_2011_shield_combined/hm_2011_sh'
#mf_name    = 'hm_2011_shield_combined_mf/hm_2011_sh'


metal_name = 'fg_2011_shield_combined/fg_2011_shield_combined'
mf_name    = 'fg_2011_shield_combined_mf/fg_2011_shield_combined_mf'
output     = 'fg_2011_shield_metal_only/fg_2011_shield_metal_only'


runs = np.arange(rmin,rmax,1)


for i in runs:
    print i
    metals = np.genfromtxt(metal_name + '_run%i.dat'%(i), names = True)
    mf     = np.genfromtxt(mf_name + '_run%i.dat'%(i), names = True)

    subtracted = metals

    subtracted['Cooling']  = metals['Cooling'] -  mf['Cooling']
    subtracted['Heating']  = metals['Heating'] -  mf['Heating']

    np.savetxt(output + '_run%i.dat'%(i), subtracted, fmt='%.6E', header = "Te Heating Cooling MMW")


