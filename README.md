# PREPARE ocean model toolbox
==============
# Developed by Knut-Frode Dagestad 
#   (MET Norway, knutfd@met.no)
# for the EU PREPARE project


This toolbox contains three Python scripts:

- get_myocean.py
    - to download ocean model data from MyOcean (Copernicus Marine Service)
- get_opendap.py
    - to download ocean model data from OPeNDAP servers
- interpolate_ocean.py
    - to interpolate downloaded NetCDF files to another map projection

The two first scripts use information about relevant datsets (and
username/password) listed in the respective files myocean_datasets.py
and opendap_datasets.py. Other datasets may be added following the
example of the datasets already included. For MyOcean datasets, it is
recommended to browse the online catalogue at www.myocean.eu in order
to become familiar with the various datasets available. For OPeNDAP
servers that require log-on credentials, insert "<userid>:<passwd>@"
after the "http://" of the url.


No installation is required, simply add this folder to your PATH to run scripts from anywhere.


Requirements:
--------------
- get_myocean.py depends on MyOcean motu-client-python,
        which is distributed within this toolbox
- get_opendap.py depends on:
        - NCO, available from http://nco.sourceforge.net
        - python-netcdf4, available from https://github.com/Unidata/netcdf4-python
- interpolate_ocean.py depends on Fimex, available from 
        http://nco.sourceforge.ne://wiki.met.no/fimex/start


Usage:
--------------

Each script requires a number of arguments. Run the scripts without arguments from the command line to get specific instructions.

Hints:
- To get an overview of the variables and dimensions contained in a dataset listed in myocean_datasets.py: Visit www.myocean.eu/web/69-myocean-interactive-catalogue.php. Use the search engine to locate the listed product and hit "MORE INFO". Select the DOCUMENTATION tab and open the PRODUCT USER MANUAL. See chapters III and V for a description of the netCDF file contents, including variable names.  
- To get an overview of the variables and dimensions contained in a dataset listed in opendap_datasets.py: Copy the url, paste it into a web browser and add ".html". The resulting listing shows the variables and their attributes, as well as facilitating a listing of the values for any variable. 
- The -v argument requires the netCDF variable name used in the datafiles (NOT the standard_name). Different datasets use different names for, e.g., the velocity components. For example, the (east,north) velocity components are named: (vozocrtx,vomecrty) for the MyOcean mediterranean datasets; (uvel,vvel) for the MyOcean baltic datasets; (water_u,water_v) for the usn_hycom datasets. See the previous hints. 
- The uppermost depth available in a particular dataset may not be at the very surface (0 m). Use a small depth range (z and Z arguments) to ensure that the uppermost data are found, e.g., "-z 0 -Z 5" will obtain all available depths in the upper 5 meters.
 

Examples:
--------------

To download one day of surface currents, temperature and ice coverage for the Gulf of Finland through MyOcean:
    ./get_myocean.py -region baltic -t 2014-12-21 12:00:00 -T 2014-12-22 12:00:00 -z Surface -Z Surface  -x 22 -X 30.2 -y 58.9 -Y 60.9 -v temp -v uvel -v vvel -v ice_cov -f gulf_finland.nc

To download one week of reanalysis upper layer currents for the Aegean Sea through MyOcean:
    ./get_myocean.py -region mediterranean -reanalysis -t 2011-11-21 00:00:00 -T 2011-11-28 12:00:00 -z 0 -Z 5  -x 22 -X 27 -y 37 -Y 41 -v vozocrtx -v vomecrty -f aegean.nc

To download all data for one day from the usn-hycom model for the Black Sea
    ./get_opendap.py -source usn-hycom -t '2014-12-25 21:00:00' -T '2014-12-26 00:00:00'  -x 40.7 -X 48.3 -y -26.5 -Y 42.3 -f blacksea.nc

To interpolate the latter data to Lambert Conformal Conic projection at 10 km grid spacing, with current components rotated to grid orientation:
    ./interpolate_ocean.py -i blacksea.nc -o blacksea_lcc.nc -proj4 "+proj=lcc +lat_1=38.69259533705237 +lat_2=39.02625053604863 +lat_0=40 +lon_0=-77.03638889 +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs" -r 10000 -v grid
