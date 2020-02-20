#============================================================
# This code reads a list of ARM observed data, samples them 
# at a coarser timestep, and then write the sampled data to 
# a new file.
#============================================================
import os
import numpy as np
from netCDF4 import Dataset as netcdf_dataset
import glob
import fnmatch

yyyy=['2016'] # list of years. NOTE: Currently not loop through years.
mm=['01'] # list of months. Only one is needed now, but can be extended.
          # ['01','02','03','04','05','06','07','08','09','10','11','12']
dd=['01','02','03','04','05','06','07','08','09','10',     \
    '11','12','13','14','15','16','17','18','19','20',     \
    '21','22','23','24','25','26','27','28','29','30','31']
ny=len(yyyy)
nm=len(mm)
nd=[31,29,31,30,31,30,31,31,30,31,30,31] #number of days in each month 

in_path='/raid00/xianwen/ARM/ARM-AWARE-DATA/awrqcrad1longM1.s2'
out_path='/raid00/xianwen/ARM/ARM-AWARE-DATA/awrqcrad1longM1.s2_rad_hourly'

# variables to be extracted. for reference only -->.
variables=['BestEstimate_down_short_hemisp','up_short_hemisp','down_long_hemisp','up_long_hemisp','zenith']  

if not os.path.exists(out_path):
     os.mkdir(out_path)

for imon in range(0,nm):
    down_sw_all=np.empty(0)
    up_sw_all=np.empty(0)
    down_lw_all=np.empty(0)
    up_lw_all=np.empty(0)
    zenith_all=np.empty(0)
    time_all=np.empty(0)
    for iday in range(0,nd[imon]):
        infile_id=glob.glob(in_path+'/*'+yyyy[0]+mm[imon]+dd[iday]+'*.cdf')
        if len(infile_id) == 0:
            continue
        infile=netcdf_dataset(infile_id[0],'r')

        down_sw_tmp=infile.variables['BestEstimate_down_short_hemisp'][0::60]
        down_sw_all=np.append(down_sw_all,down_sw_tmp)

        up_sw_tmp=infile.variables['up_short_hemisp'][0::60]
        up_sw_all=np.append(up_sw_all,up_sw_tmp)

        down_lw_tmp=infile.variables['down_long_hemisp'][0::60]
        down_lw_all=np.append(down_lw_all,down_lw_tmp)

        up_lw_tmp=infile.variables['up_long_hemisp'][0::60]
        up_lw_all=np.append(up_lw_all,up_lw_tmp)

        zenith_tmp=infile.variables['zenith'][0::60]
        zenith_all=np.append(zenith_all,zenith_tmp)

        time_tmp=infile.variables['time'][0::60]
        time_tmp=sum(nd[0:imon])+iday+1+np.around(time_tmp/(24.*60.*60.),decimals=5)
        time_all=np.append(time_all,time_tmp)

        lat_now=infile.variables["lat"][:]
        lon_now=infile.variables["lon"][:]

    #create output file
    outfile=out_path+'/awrqcrad1longM1.s2.rad.hourly.'+yyyy[0]+mm[imon]+'.nc'
    ncfile=netcdf_dataset(outfile,'w')
    #-create dimention
    #print(infile.dimensions.items())
    time_dim=ncfile.createDimension('time',None)
    #-create variables
    time=ncfile.createVariable('time',np.float64,('time',))
    time.units='days since '+yyyy[0]+mm[0]+"01 00:00"
    time.long_name='time'
 
    lat=ncfile.createVariable('lat',np.float64)
    lat.long_name='North latitude'
    lat.units='degree_N'
    lat.valid_min=-90.0
    lat.valid_max=90.0
    lat.standard_name='latitude'

    lon=ncfile.createVariable('lon',np.float64)
    lon.long_name='East longitude'
    lon.units='degree_E'
    lon.valid_min=-180.0
    lon.valid_max=180.0
    lon.standard_name='longitude'

    down_sw=ncfile.createVariable('BestEstimate_down_short_hemisp',np.float64,('time'))
    up_sw=ncfile.createVariable('up_short_hemisp',np.float64,('time'))
    down_lw=ncfile.createVariable('down_long_hemisp',np.float64,('time'))
    up_lw=ncfile.createVariable('up_long_hemisp',np.float64,('time'))
    zenith=ncfile.createVariable('zenith',np.float64,('time'))

    down_sw.units='W/m^2'
    down_sw.long_name='Best Estimate Global Downwelling Shortwave Hemispheric Irradiance'
    down_sw.standard_name='surface_downwelling_shortwave_flux_in_air'
    down_sw.missing_value=-9999.0

    up_sw.units='W/m^2'
    up_sw.long_name='Upwelling Shortwave Hemispheric Irradiance'
    up_sw.standard_name='surface_upwelling_shortwave_flux_in_air'
    up_sw.missing_value=-9999.0

    down_lw.units='W/m^2'
    down_lw.long_name='Downwelling (10 meter) Longwave Hemispheric Irradiance'
    down_lw.standard_name='surface_downwelling_longwave_flux_in_air'
    down_lw.missing_value=-9999.0

    up_lw.units='W/m^2'
    up_lw.long_name='Upwelling (10 meter) Longwave Hemispheric Irradiance'
    up_lw.standard_name='surface_upwelling_longwave_flux_in_air'
    up_lw.missing_value=-9999.0

    zenith.units='degree'
    zenith.long_name='Solar Zenith Angle'
    zenith.standard_name='solar_zenith_angle'
    zenith.comment='Calculated using solarposition() function, by Nels Larson, PNNL'

    #-write data
    down_sw[:]=down_sw_all[:]
    up_sw[:]=up_sw_all[:]
    down_lw[:]=down_sw_all[:]
    up_lw[:]=down_sw_all[:]
    zenith[:]=zenith_all[:]
    time[:]=time_all[:]
    lat[:]=lat_now
    lon[:]=lon_now
    #-all finished, close the file
    ncfile.close()     
#print(time_all)

#=====
# END
#=====
