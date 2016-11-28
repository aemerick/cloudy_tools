import numpy as np

nz = 25
dz = nz

metals = False

cr_dr = ncr_dr = ot_dir = ' '

output = '-'

if metals:
    cr_dir  = 'hm_2011_sh_final_CR/'
    ncr_dir = 'hm_2011_sh_final/'
    ot_dir  = 'hm_2011_nosh_metals/'
    output = 'hm_2011_shield_combined/'
else:
    cr_dir  = 'hm_2011_sh_final_mf_CR/'
    ncr_dir = 'hm_2011_sh_final_mf/'
    ot_dir  = 'hm_2011_nosh/'
    output = 'hm_2011_shield_combined_mf/'

hdens = np.arange(-10, 4.5, 0.5)


metal_crdir = 'hm_2011_sh_final_CR/'
metal_ncrdir = 'hm_2011_sh_final/'
metal_otdir = 'hm_2011_nosh_metals/'

for zi in np.arange(1, nz+1):

    print zi

    for index in np.arange(np.size(hdens)):
        i = zi + dz*index

#        if hdens[index] <= 2.0 or not metals: # normal things for low density or non-metal
        if hdens[index] <= 2.0:

            cr_data  = np.genfromtxt(cr_dir + 'hm_2011_sh_run%i.dat'%(i), skip_header = 14, names = True)
            ncr_data = np.genfromtxt(ncr_dir + 'hm_2011_sh_run%i.dat'%(i), skip_header = 14, names=True)
            ot_data  = np.genfromtxt(ot_dir + 'hm_2011_run%i.dat'%(i), skip_header = 14, names = True)


            metal_crdata = np.genfromtxt(metal_crdir + 'hm_2011_sh_run%i.dat'%(i), skip_header = 14, names =True)
            metal_ncrdata = np.genfromtxt(metal_ncrdir + 'hm_2011_sh_run%i.dat'%(i), skip_header = 14, names=True)
            metal_otdata  = np.genfromtxt(metal_otdir + 'hm_2011_run%i.dat'%(i), skip_header = 14, names=True)

            #
            # start using data with most temperature coverage
            #


#
#
#             doing some crazy stuff to stich metal free together such that metal free is always matched with same
#             physics as metal tables
#

#            sizes = np.array([np.size(cr_data['Te']) , np.size(ncr_data['Te']), np.size(ot_data['Te'])])
            sizes = np.array([np.size(metal_crdata['Te']) , np.size(metal_ncrdata['Te']), np.size(metal_otdata['Te'])])

            data   = [cr_data, ncr_data, ot_data]

            output_data = data[ sizes.argmax() ]

            if hdens[index] <= -8.5:
                # may need to use metal free data here
                if np.max(sizes) < 161:
                    # use optically thin metal free data, and progressively overwrite with other things
                    ot_mf = np.genfromtxt('hm_2011_nosh/hm_2011_run%i.dat'%(i), skip_header = 14, names=True)

                    output_data = ot_mf
                    if metals:
                        for name in ['Te','Cooling','Heating','MMW']:
                            output_data[name][:np.size(metal_otdata['Te'])] = ot_data[name][:np.size(metal_otdata['Te'])]
                    for name in ['Te','Cooling','Heating','MMW']:
                        output_data[name][:np.size(metal_ncrdata['Te'])] = ncr_data[name][:np.size(metal_ncrdata['Te'])]
                    for name in ['Te','Cooling','Heating','MMW']:
                        output_data[name][:np.size(metal_crdata['Te'])] = cr_data[name][:np.size(metal_crdata['Te'])]

            else:

                # now use CR shielding data to supercede when possible
                # when not possible, use non CR data to supercede, but make sure using as
                # much CR as possible
                if (np.size(metal_crdata['Te']) >= np.size(metal_ncrdata['Te'])):
                    for name in ['Te','Cooling','Heating','MMW']:
                        output_data[name][:np.size(metal_crdata['Te'])]  = cr_data[name][:np.size(metal_crdata['Te'])]
                else:
                    for name in ['Te','Cooling','Heating','MMW']:
                        output_data[name][:np.size(metal_ncrdata['Te'])] = ncr_data[name][:np.size(metal_ncrdata['Te'])]

                    for name in ['Te','Cooling','Heating','MMW']:
                        output_data[name][:np.size(metal_crdata['Te'])] = cr_data[name][:np.size(metal_crdata['Te'])]
        else:
            # cr data does not exist... to long to make
            ncr_data = np.genfromtxt(ncr_dir + 'hm_2011_sh_run%i.dat'%(i), skip_header = 14, names=True)
            ot_data  = np.genfromtxt(ot_dir + 'hm_2011_run%i.dat'%(i), skip_header = 14, names = True)

            #
            # start using data with most temperature coverage
            #
            output_data = ot_data

            # now use CR shielding data to supercede when possible
            # when not possible, use non CR data to supercede, but make sure using as
            # much CR as possible
            for name in ['Te','Cooling','Heating','MMW']:
                output_data[name][:np.size(ncr_data)] = ncr_data[name]

#            for name in ['Cooling','Heating','MMW']:
#                output_data[name][ output_data['Te'][np.size(cr_data['Te'])] == cr_data['Te']] = cr_data[name]


        np.savetxt(output + 'hm_2011_sh_run%i.dat'%(i), output_data, fmt='%.6E', header = "Te Heating Cooling MMW")
