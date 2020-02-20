# ARM_data_for_3D_Rad
This contains ARM-AWARE observed/reanalysis data for 3D radiation calculation and comparison. 
The input data are derived from ECWMF reanalysis (Wuyin Lin, BNL), and the radiation observations are from QCRAD product (https://www.arm.gov/capabilities/vaps/qcrad). The data have a timestep of 1-hour, during January 2016.

Input data for radiation model is in SCM_IOP. Variables include: 
     T, Q, T_ground, P_lev, albedo, cloud_liq, cloud_ice, cloud_fraction, Relative_humidity.
Observed radiation data is in awrqcrad1longM1.s2_rad_hourly. Variables include:
     down_sw_surface, up_sw_surface, down_lw_surface, up_lw_surface, solar_zenith_angle
