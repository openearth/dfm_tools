dfm_tools
=========

dfm_tools are Python post-processing tools for Delft3D FM model outputfiles and other netCDF files

- Free software: GNU General Public License v3


Table of contents
--------
<!--ts-->
   * [Features](#features)
   * [Installation](#installation)
   * [Example usage](#example-usage)
   * [Feature wishlist](#feature-wishlist)
   * [Todo non-content](#todo-non-content)
   * [Developer information](#developer-information)
<!--te-->


Features
--------
- supported formats:
	- D-Flow FM output data (net, map, his, fou, rst files)
	- almost any other netCDF (ERA5, hirlam, SFINCS map, SFINCS his, Sobek observation)
	- Delft3D netCDF output files (you can get netcdf output with keywords in your mdf)
	- converted Delft3D and waqua data (converted to netCDF with getdata.pl) (Delft3D conversion with getdata.pl is not flawless, preferably rerun with netCDF as outputformat instead)
- data handling:
	- support for net/map/fou/rst partitions
	- support for flexible meshes (containing triangles, squares, pentagons, hexagons or any other shape)
	- select all data based on variable, timestep/datetime, layer, station (not yet on depth)
	- get feedback about available variables, timesteps/datetimes, layers, stations when you retrieve the wrong ones
	- retrieve lists of variables, timesteps/datetimes, stations, cross sections, general structures
	- selection/plotting by polyline/crossection (slicing the ugrid data)
	- merge partitions and delete ghostcells automatically
	- take over masks in original data
	- retrieve/select any data you want, including metadata consisting of retrieved timeids/datetimes, stationids/stationnames and layerids
- plotting:
	- plot flexible mesh net/map variables as polycollections/patches
	- plot regular grid variables with pcolor (precise plotting is still work in progress)
	- plot cartopy features (land, sea, landboundary, country borders, satellite background)
	- plotting z,t-plots (see [Feature wishlist](#feature-wishlist) for known inaccuracies)
	- plot any data you want and exactly how you want it
- other io functions:
	- read tekal data (.tek, .pli, .pliz, .pol, .ldb)
	- read/write mdu file
	- read/write bc file
	- write model results to shapefile
- html documentation:
	- https://htmlpreview.github.io/?https://github.com/openearth/dfm_tools/blob/master/doc/dfm_tools/index.html

Installation
--------
- download Anaconda 64 bit Python 3.7 from https://www.anaconda.com/distribution/#download-section (miniconda is probably also sufficient, but this is not yet tested)
- install it with the recommended settings, but check 'add Anaconda3 to my PATH environment variable' if you want to use conda from the windows command prompt instead of anaconda prompt
- install dfm_tools from github:
	- open command window (or anaconda prompt)
	- ``conda create --name dfm_tools_env -c conda-forge python=3.7 git spyder -y``
	- ``conda activate dfm_tools_env``
	- ``python -m pip install git+https://github.com/openearth/dfm_tools.git`` (this command installs dfm_tools and all required packages)
	- optional: ``conda install -c conda-forge "shapely>=1.7.0" -y`` (for slicing 2D/3D data) (conda-forge channel is necessary since main channel version is 1.6.4)
	- optional: ``conda install -c conda-forge cartopy -y`` (for satellite imagery, coastlines etc on plots) (conda-forge channel recommended by cartopy developers, and currently also necessary for correct shapely version)
	- optional: ``conda install -c conda-forge geopandas -y`` (for shapefile related operations)
	- optional: ``conda install -c conda-forge contextily -y`` (for satellite imagery on plots, seems faster than cartopy)
	- to remove venv when necessary: ``conda remove -n dfm_tools_env --all``
- launch Spyder:
	- open 'Spyder(dfm_tools_env)' via your windows start menu (not 'Spyder' or 'Spyder(Anaconda3)', since dfm_tools was installed in dfm_tools_env)
	- if launching Spyder gives a Qt related error: remove the system/user environment variable 'qt_plugin_path' set by an old Delft3D4 installation procedure
	- test by printing dfm_tools version number: ``import dfm_tools; print(dfm_tools.__version__)`` (to double check if you are working in the venv where dfm_tools_env was installed)
	- to get figures in separate windows: go to Tools > Preferences > IPython console > Graphics > change graphics backend to 'Automatic' and restart Spyder (or the kernel).
	- copy the code from [Example usage](#example-usage) to your own scripts to get starteds
- to update dfm_tools:
	- open command window (or anaconda prompt)
	- ``conda activate dfm_tools_env``
	- ``python -m pip install --upgrade git+https://github.com/openearth/dfm_tools.git``


Example usage
--------
- for more examples, check https://github.com/openearth/dfm_tools/tree/master/tests (this is also the pytest testbank)
- examples of (mostly unformatted) figures created by this pytest testbank: n:\\Deltabox\\Bulletin\\veenstra\\info dfm_tools
- please check the [Feature wishlist](#feature-wishlist) for envisioned features
- please report bugs and feature requests at the developers or at https://github.com/openearth/dfm_tools/issues (include OS, dfm_tools version, reproduction steps)
- want to get updates about dfm_tools? Send an email to jelmer.veenstra@deltares.nl

```python
#data retrieval is easy, just use get_ncmodeldata() with file_nc argument
#then use the feedback in the error messages to set other arguments like varname, timestep, station and layer
from dfm_tools.get_nc import get_ncmodeldata
data_fromnc = get_ncmodeldata(file_nc='yourfile.nc')
```

```python
#the below example includes plotting and using the metadata of the retrieved data
#import statements
import os
import matplotlib.pyplot as plt
plt.close('all')
from dfm_tools.get_nc import get_netdata, get_ncmodeldata, plot_netmapdata
from dfm_tools.get_nc_helpers import get_ncvardimlist, get_timesfromnc, get_hisstationlist

#uncomment the line below, copy data locally and change this path to increase performance
#dir_testinput = os.path.join(r'n:\Deltabox\Bulletin\veenstra\info dfm_tools\test_input')
file_nc_map = os.path.join(dir_testinput,'DFM_sigma_curved_bend','DFM_OUTPUT_cb_3d','cb_3d_map.nc')
file_nc_his = os.path.join(dir_testinput,'DFM_sigma_curved_bend','DFM_OUTPUT_cb_3d','cb_3d_his.nc')

#get lists with vars/dims, times, station/crs/structures
vars_pd, dims_pd = get_ncvardimlist(file_nc=file_nc_map)
times_pd = get_timesfromnc(file_nc=file_nc_map)
statlist_pd = get_hisstationlist(file_nc=file_nc_his, varname='station_name')

#retrieve his data
data_fromhis_wl = get_ncmodeldata(file_nc=file_nc_his, varname='waterlevel', station='all', timestep= 'all')
fig, ax = plt.subplots(1,1,figsize=(10,5))
for iP, station in enumerate(data_fromhis_wl.var_stations['station_name']):
    ax.plot(data_fromhis_wl.var_times,data_fromhis_wl[:,iP],'-', label=station)
ax.legend()
ax.set_ylabel('%s (%s)'%(data_fromhis_wl.var_varname, data_fromhis_wl.var_ncvarobject.units))

#plot net/grid
ugrid_all = get_netdata(file_nc=file_nc_map)#,multipart=False)
fig, ax = plt.subplots()
pc = plot_netmapdata(ugrid_all.verts, values=None, ax=None, linewidth=0.5, color="crimson", facecolor="None")
ax.set_aspect('equal')

#plot water level on map
data_frommap_wl = get_ncmodeldata(file_nc=file_nc_map, varname='mesh2d_s1', timestep=3)#, multipart=False)
fig, ax = plt.subplots()
pc = plot_netmapdata(ugrid_all.verts, values=data_frommap_wl[0,:], ax=None, linewidth=0.5, cmap="jet")
pc.set_clim([-0.5,1])
fig.colorbar(pc, ax=ax)
ax.set_title('%s (%s)'%(data_frommap_wl.var_varname, data_frommap_wl.var_ncvarobject.units))
ax.set_aspect('equal')

#plot salinity on map
data_frommap_sal = get_ncmodeldata(file_nc=file_nc_map, varname='mesh2d_sa1', timestep=2, layer=5)#, multipart=False)
fig, ax = plt.subplots()
pc = plot_netmapdata(ugrid_all.verts, values=data_frommap_sal[0,:,0], ax=None, linewidth=0.5, cmap="jet")
fig.colorbar(pc, ax=ax)
ax.set_title('%s (%s)'%(data_frommap_sal.var_varname, data_frommap_sal.var_ncvarobject.units))
ax.set_aspect('equal')

#print contents of retrieved data withing data_frommap_sal variable
print_var = data_frommap_sal
print('++++++\nthe data in the variable %s is:\n%s\n'%(print_var.var_varname, print_var))
print('++++++\nthe time indices and times in the variable %s are:\n%s\n'%(print_var.var_varname, print_var.var_times))
print('++++++\nthe station indices and station names in the variable %s are:\n%s\n'%(print_var.var_varname, print_var.var_stations))
print('++++++\nthe layer indices in the variable %s are:\n%s\n'%(print_var.var_varname, print_var.var_layers))
print('++++++\nthe shape of the variable %s is:\n%s\n'%(print_var.var_varname, print_var.shape))
print('++++++\nthe dimensions of the variable %s are (copied from netCDF variable):\n%s\n'%(print_var.var_varname, print_var.var_dimensions))
print('++++++\nthe netCDF variable where the data in variable %s comes from is:\n%s\n'%(print_var.var_varname, print_var.var_ncvarobject))
print('++++++\nsome example contents of this netCDF variable:')
print('\tthe dimension names of the netCDF variable %s are:\n\t\t%s'%(print_var.var_varname, print_var.var_ncvarobject.dimensions))
print('\tthe shape of the netCDF variable %s is:\n\t\t%s'%(print_var.var_varname, print_var.var_ncvarobject.shape))
print('\tthe units of the netCDF variable %s are:\n\t\t%s'%(print_var.var_varname, print_var.var_ncvarobject.units))
print('\tthe long_name of the netCDF variable %s is:\n\t\t%s'%(print_var.var_varname, print_var.var_ncvarobject.long_name))
print('\tthe standard_name of the netCDF variable %s is:\n\t\t%s'%(print_var.var_varname, print_var.var_ncvarobject.standard_name))
```


Feature wishlist
--------
- use isinstance for dtype testing in get_nc()
- correct timezone in netCDF to UTC or not, keyword?
- integrate values_all and values_all_topbot in get_nc(), avoid concatenating to empty (size 0) array of values_all is a first step
- improve time reading:
	- add support for 360_day and noleap calendars (cannot be converted to dt.datetime)
	- time array is now converted to UTC by num2date automatically and if possible converted back to original timezone, simplify by writing own num2date that excludes timezone from units strin?
- merge station/layer/times checks, these parts of get_nc.py have a lot of overlap. also convert (list-likes of) int-likes to np.arrays so less checking is needed
- add retrieval via depth instead of layer number (then dflowutil.mesh can be removed?):
	- refer depth w.r.t. reference level, water level or bed level
	- see test_workinprogress.py
	- see general grid improvement options
- retrieve correct depths:
	- add depth array (interfaces/centers) to his and map variables (z/sigma layer calculation is already in get_modeldata_onintersection function)
	- depths can be retrieved from mesh2d_layer_z/mesh2d_layer_sigma, but has no time dimension so untrue for sigma and maybe for z? (wrong in dflowfm?)
	- layerzfrombedlevel keyword in mdu changes how zlayering is set up. Catch this exception with a keyword if necessary
	- support for mixed sigma/z layers?
- plotting:
	- simplify input of modplot.velovect() for curved vectors
	- contour plot of surfaces (e.g. cotidal chart), with polycollection (FM grid) or regular grid, exclude 'land' (shapely overlap between cells of two grids? or create polygon around all edges of original grid (also islands) and use that to cut the resulting regular grid)
- improve z,t-plots from hisfile:
	- example in test_get_nc.test_gethismodeldata()
	- WARNING: part of the z interfaces/center data in dflowfm hisfile is currently wrong, check your figures carefully. Most of it is handled correctly
	- layer argument now has to be provided when retrieving zcoordinate_c (centers) from hisfile, but not when retrieving zcoordinate_w (interfaces), align this.
- export to shapefile:
	- testbank example added for a specific feature to shapefile, make more generic
- coordinate conversion:
	```python
	from pyproj import Proj, transform
	inProj = Proj(init='epsg:%i'%(epsg_in))
	outProj = Proj(init='epsg:%i'%(epsg_out))
	x_out,y_out = transform(inProj,outProj,x_in,y_in)
	```
- add more io-functions:
	- read/write matroos data (first setup in dfm_tools.io.noos)
	- convert data to kml (google earth) or shp? (including RD to WGS84 conversion and maybe vice versa)
	- improve tekal map read
	- add tekal mergedatasets function to get e.g. one ldb dataset with the original parts separated with nans
	- add tekal write functions
- add tidal analysis:
	- https://github.com/sam-cox/pytides
	- https://pypi.org/project/pytides/
	- https://github.com/pwcazenave/tappy
	- https://pypi.org/project/UTide/
	- https://github.com/moflaher/ttide_py
	- hatyan
- make merc keyword always optional by testing for minmax all vertsx between -181 and 361 and minmax all vertsy (lat) between -91 and 91 (+range for overlap for e.g. gtsm model)
- improve get_ncmodeldata second intersect function
	- optimize with distance from line: get maximum cell area (and infer width) from lineblockbbound selection, then decide on distance from line for selection of cells for crossect calculation
	- optimize by only retrieving necessary layerdepths/bed/waterlevel information for crossection
	- remove hardcoded (layer/)bed/waterlevel varnames
- add inpolygon/inboundbox selection of data:
	- optimize_dist keyword now draws inpolygon around line
	- to optimize intersect function when retrieving bed level and water level (do that with len(firstlinepart) optional keyword)
	- to retrieve other mapdata data faster
- add polygon ginput function (click in plot) (already partly exists in intersect/slice testscript)
- merge existing dfm model setup functions (and other useful stuff):
	- dflowutil: https://github.com/openearth/dfm_tools/tree/master/dflowutil (and test scripts, contains e.g. read/write functions for general datafromats (like tim))
	- MBay scripts
	- https://github.com/openearth/delft3dfmpy (arthur van dam)	
	- https://svn.oss.deltares.nl/repos/openearthtools/trunk/python/applications/delft3dfm (fiat, sobek etc)
	- https://svn.oss.deltares.nl/repos/openearthtools/trunk/python/applications/delft3dfm/dflowfmpyplot/pyd3dfm/streamline_ug.py (streamline plotting for structured grids, but many settings)
- make grid reading more flexible:
	- raise understandable error when no mesh2d_edge_x var in netcdf, instead of keyerror none (e.g. with get_netdata on hirlam files)
	- if no ugrid in netfile, try to read provided xy variables and make meshgrid or convert cen2cor or cor2cen if necessary (how to test this?)
	- improve plots for structured grid (CMEMS, ERA5, hirlam, grd etc)
	- https://github.com/NOAA-ORR-ERD/gridded (https://github.com/pyugrid/pyugrid is merged into gridded) (ghostcells en mapmergen worden afgehandeld? meer dan 4 nodes per cel? support for stations?)
	- gridded presentatie: https://ams.confex.com/ams/97Annual/webprogram/Handout/Paper312839/Barker_AMS-2017.pdf
	- tests.test_get_nc.test_getnetdata_plotnet_regular() is eerste opzet voor hirlam/ERA5 data, werkt heel anders dan D-flow FM
	- how to plot properties on edges/nodes (scatter is slow), maybe create dual mesh and plot like faces. most relevant variables are also available on faces, so is this necessary?
	- improve support for rstfiles (now only scatter, since only cell centers present?)
	- https://svn.oss.deltares.nl/repos/openearthtools/trunk/python/OpenEarthTools/openearthtools/io/dflowfm/patch2tri.py (equivalent van MIA)
	- https://svn.oss.deltares.nl/repos/openearthtools/trunk/python/OpenEarthTools/openearthtools/io/netcdf
	- plotting edges/nodes/faces and legend: https://github.com/pyugrid/pyugrid/blob/master/notebook_examples/connectivity_example.ipynb
	- add retrieve_netdata argument to get_ncmodeldata() which causes griddata to be retrieved as the second return variable (do this based on coordinates / cf-conventions)?
	- pcolor resulteert ook in een polycollection, net zoals handmatig wordt gedaan met plot_mapdata()
	- implement kivu paper figure in testbank, since it correctly combines m/n corners with mapdata (including dummy row)
	- possible to add pyugrid from github as dependency? in setup.py: install_requires=['python_world@git+https://github.com/ceddlyburge/python_world#egg=python_world-0.0.1',]
	- sigma method in get_xzcoords_onintersection() is assumes equidistant layers, add exception
	- zlayer method in get_xzcoords_onintersection() retrieves from hardcoded interface variable name, centers are not used.
	- how is depth stored in sigma/z/sigma-z models, generic vertical slice method possible?
- interactive data retrieval and plotting by calling get_ncmodeldata() without arguments


Todo non-content
--------
- improve communication material:
	- add variable units to plots in test bench
	- improve his plots and tekal map plots, improve other plots
	- put testdata and testoutput on github and create jupyter notebook instead of pptx?
	- create overview of scripts and functions, including future location of missing features
	- write documentation as comments (docstrings) and generate html documentation automatically with pdoc (or maybe sphinx?)
	- improve feedback to user if no or wrong input arguments are given to functions
	- add license to new scripts
- external improvements:
	- fix small bugs in Delft3D4 netCDF output (related to coordinates, coordinates of velocity points and incorrect missing values)
	- request modplot.velovect() (curved vectors) to be added to matplotlib
	- install without PATH fails on pip/git in anaconda prompt? (test installation with anaconda prompt, and with command prompt combined with ``set PATH=%PATH%;<your_path_to_anaconda_installation>\Scripts``)
	- installation also possible with miniconda only?
- register on PyPI, for easier install via pip (easier for regular users):
	- https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/quickstart.html#register-your-package-with-the-python-package-index-pypi
	- https://packaging.python.org/tutorials/packaging-projects/
	- how to automate this process? (buildserver including testing?)
	- also add changelog besides commit comments?
	- alternatively, register on conda-forge: https://github.com/conda-forge/staged-recipes/
- put testdata on deltares shared location?
- arrange auto-testing online (jarvis?): https://docs.pytest.org/en/latest/getting-started.html
- update license with Deltares terms
- style guide: https://www.python.org/dev/peps/pep-0008/
- contributing environment method: environment.yml or requirements_dev.txt?


Developer information
--------
- How to contribute to this git repository?
- First request github rights to contribute with the current developers:
	- Jelmer Veenstra <jelmer.veenstra@deltares.nl>
	- Lora Buckman
	- Julien Groenenboom
- Get a local checkout of the github repository:
	- Download git from https://git-scm.com/download/win, install with default settings
	- open command window in a folder where you want to clone the dfm_tools github repo, e.g. C:\\DATA
	- ``git clone https://github.com/openearth/dfm_tools.git`` (repos gets cloned in C:\\DATA\\dfm_tools, this is a checkout of the master branch)
	- open git bash window in local dfm_tools folder (e.g. C:\\DATA\\dfm_tools)
	- ``git config --global user.email [emailaddress]``
	- ``git config --global user.name [username]``
	- create a branch called work_yourname on https://github.com/openearth/dfm_tools
	- open git bash window in local dfm_tools folder (e.g. C:\\DATA\\dfm_tools)
	- ``git remote update origin --prune`` (update local branch list)
	- ``git checkout work_yourname`` (checkout your branch, never do anything while the master is selected)
- Set up the dfm_tools developer python virtual environment (necessary for developing/testing):
	- open command window (or anaconda prompt) and navigate to dfm_tools folder, e.g. C:\\DATA\\dfm_tools
	- ``conda env create -f environment.yml`` (creates an environment called dfm_tools_devenv)
	- to list venvs:``conda info --envs``
	- to remove venv when necessary: ``conda remove -n dfm_tools_devenv --all``
	- ``conda activate dfm_tools_devenv``
	- ``python -m pip install -e .`` (pip developer mode, any updates to the local folder by github (with ``git pull``) are immediately available in your python. It also installs all required packages)
	- ``conda install -c conda-forge spyder "shapely>=1.7.0" cartopy geopandas contextily``(conda-forge channel is necessary since main channel shapely version is 1.6.4. The correct version is available via pip, but then geos dll is not properly linked, this will probably be solved in the future https://github.com/Toblerity/Shapely/issues/844. cartopy also recommends conda-forge channel)
	- test if dfm_tools is properly installed by printing the version number: ``python -c "import dfm_tools; print(dfm_tools.__version__)"``
	- open 'Spyder(dfm_tools_devenv)' via your windows start menu (not 'Spyder' or 'Spyder(Anaconda3)', since dfm_tools was installed in dfm_tools_devenv)
- Make your local changes to dfm_tools
- Work with your branch:
	- open git bash window in local dfm_tools folder (e.g. C:\\DATA\\dfm_tools)
	- ``git checkout work_yourname`` (checkout your branch, never do anything while the master is selected)
	- to update: ``git pull`` (combination of git fetch and git merge)
	- get clean checkout again (overwrite local changes):
		- ``git fetch --all`` (fetches changes)
		- ``git reset --hard`` (resets local checkout of repos branch to server version)
		- ``git pull`` (fetches and merges changes, local checkout of repos branch is now updated again)
	- ``git pull origin master`` (gets edits from master to current local branch, might induce conflicts. maybe better to just push to your branch and then handle pull request on github website)
- run test bank:
	- open command window (or anaconda prompt) in local dfm_tools folder (e.g. C:\\DATA\\dfm_tools)
	- ``conda activate dfm_tools_devenv``
	- ``pytest -v --tb=short`` (runs all tests)
	- ``pytest -v --tb=short -m unittest``
	- ``pytest -v --tb=short -m systemtest``
	- ``pytest -v --tb=short -m acceptance``
	- ``pytest -v --tb=short tests\test_get_nc.py::test_getplotmapWAQOS``
- Regenerate html documentation:
	- open command window (or anaconda prompt) in local dfm_tools folder (e.g. C:\\DATA\\dfm_tools)
	- ``conda activate dfm_tools_devenv``
	- ``pdoc --html dfm_tools -o doc --force``
- Commit and push your changes to your branch:
	- open git bash window in local dfm_tools folder (e.g. C:\\DATA\\dfm_tools)
	- ``git checkout work_yourname`` (checkout your branch, never do anything while the master is selected)
	- ``git add .``
	- ``git commit -m "message to be included with your commit"``
	- ``git push`` (pushes changes to server, do not do this in while working in the master)
- increasing the version number after you committed all changes:
	- open cmd window in local dfm_tools folder (e.g. C:\\DATA\\dfm_tools)
	- optional: ``conda activate dfm_tools_devenv``
	- ``bumpversion major`` or ``bumpversion minor`` or ``bumpversion patch`` (changes version numbers in files and commits changes)
	- push this change in version number with ``git push`` (from git bash window or cmd also ok?)
- Request merging of your branch on https://github.com/openearth/dfm_tools/branches

