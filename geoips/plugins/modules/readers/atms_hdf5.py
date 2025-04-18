# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""Reader to read a grannual NOAA ATMS SDR TBs in h5 format.

Output variables in xarray object for geoips processing system

V0:   August 25, 2021

The date is generated by the NOAA community satellite processing package
(CSPP), developed at CIMSS

Example of ATMS file names::

    'SATMS_j01_d20210809_t0959306_e1000023_b19296_fnmoc_ops.h5'
        SDR TBs variables
    'GATMO_j01_d20210809_t0959306_e1000023_b19296_fnmoc_ops.h5'
        SDR Geolocation variables

Dataset info::

    TB[12,96,22]:  for each granuel

    CHAN#  Center-Freq(GHz)  POL
    1      23.8               V
    2      31.4               V
    3      50.3               H
    4      51.76              H
    5      52.8               H
    6      53.596+-0.115      H
    7      54.4               H
    8      54.94              H
    9      55.5               H
    10     57.290(f0)         H
    11     f0 +-0.217         H
    12     f0 +-0.322+-0.048  H
    13     f0 +-0.322+-0.022  H
    14     f0 +-0.322+-0.010  H
    15     f0 +-0.322+-0.0045 H

    16     88.2               V
    17     165.5              H
    18     183.1+-7           H
    19     183.1+-4.5         H    (FNMOC used this chan for 183 GHz image)
    20     183.1+-3.0         H
    21     183.1+-1.8         H
    22     183.1+-1.0         H

    BeamTime[12,96]:  microsecond, i.e., 1*10^-6.  IET "IDPS Epoch Time" is used
                      It is a signed 64-bit integer giving microseconds since
                      00:00:00.000000 Jan 1 1958.
    BrightnessTemperatureFactors[2]: 1: scale (unitless); 2: offset (K)
    BrightnessTemperature[12,96,22]: [scan,pix,chans]

    SDR geolocation Info
    Latitude/Longitude[12,96]:   for Chan 17 only (for initial product,
                                                   it is used for all channels)
    BeamLatitude[12,96,5]:       for chan 1,2,3,16,17. They will be used for
                                            associated TBs at a later date.
    BeamLongitude[12,96,5]:      for chan 1,2,3,16,17
    SatelliteAzimuthAngle, SatelliteZenithAngle,
    SolarAzimuthAngle, SolarZenithAngle[12,96]

Notes
-----
Unix epoch time is defined as the number of seconds that have elapsed
since January 1, 1970 (midnight UTC/GMT). Thus, there is a 12 years
difference for the JPSS data when
datetime.datetime.utcfromtimestamp(epoch) is used
to convert the JPSS IDPS Epoch time to the humman-readable date.

This reader is developed to read one granual a time from ATMS npp and
jpss-1(n20) data files.

The example files are:

* ``SATMS_j01_d20210809_t0959306_e1000023_b19296_fnmoc_ops.h5``: for TBs.  'b': orbit#
* ``GATMO_j01_d20210809_t0959306_e1000023_b19296_fnmoc_ops.h5``: for geolocations
"""

# Python Standard Libraries
import datetime
import logging
from os.path import basename

# Third-Party Libraries
from astropy.time import Time
from dateutil.relativedelta import relativedelta
import h5py
import numpy as np
import xarray as xr

LOG = logging.getLogger(__name__)

interface = "readers"
family = "standard"
name = "atms_hdf5"
source_names = ["atms"]

# from IPython import embed as shell

# list of variables selected from input files
atms_vars = [
    "BrightnessTemperature",
    "BrightnessTemperatureFactors",
    "BeamTime",
    "Latitude",
    "Longitude",
    "SatelliteAzimuthAngle",
    "SatelliteZenithAngle",
    "SolarAzimuthAngle",
    "SolarZenithAngle",
    "StartTime",
]

# unify common names for sat/sun-zenith and azimuth angles
xvarnames = {
    "SolarZenithAngle": "solar_zenith_angle",
    "SolarAzimuthAngle": "solar_azimuth_angle",
    "SatelliteZenithAngle": "satellite_zenith_angle",
    "SatelliteAzimuthAngle": "satellite_azimuth_angle",
}

# final_xarray = xr.Dataset()  # define a xarray to hold all selected variables


def convert_epoch_to_datetime64(time_array, use_shape=None):
    """Convert time to datetime object.

    Parameters
    ----------
    time_array : array
        Array of start time integers (multiplied by 1e-6 in function)
    use_shape : tuple, optional
        desired output shape of time array, by default None

    Returns
    -------
    array
        array of converted datetime objects
    """
    # Convert TAI to UTC using astropy
    utc_time = Time(time_array / 1e6, format="unix_tai").utc.datetime

    # ATMS Epoch starts at 1958-01-01, not 1970-01-01
    utc_time -= relativedelta(years=12)

    # Either convert 1D array to 2D, or return original shape
    if time_array.ndim == 1 and use_shape:
        nscan, npix = use_shape
        converted_time = np.zeros((nscan, npix)).astype(datetime.datetime)
        for i in range(nscan):
            converted_time[i, :] = utc_time[i]
    else:
        converted_time = utc_time

    return converted_time.astype(np.datetime64)


def read_atms_file(fname, xarray_atms, metadata_only=False):
    """Read ATCF data from file fname."""
    fileobj = h5py.File(fname, mode="r")

    # check for available variables from nput file
    # Do not read the BT data unless metadata_only is False
    if "ATMS-SDR_All" in fileobj["All_Data"].keys():  # for TB-data
        data_select = fileobj["All_Data"]["ATMS-SDR_All"]

        tb_time = data_select["BeamTime"][()]
        #  get UTC time in datetime64 format required by geoips for each pixel
        time_scan = convert_epoch_to_datetime64(tb_time)

        # Rather than reading from the file, create empty arrays of time_scan shape
        if metadata_only:
            V23 = V31 = H50 = V89 = H165 = H183 = np.empty(time_scan.shape)
        else:
            tb = data_select["BrightnessTemperature"][()]
            tb_factor = data_select["BrightnessTemperatureFactors"][()]

            # convert tb to actual values
            tbs = tb * tb_factor[0] + tb_factor[1]

            # TBs for selected channels
            V23 = tbs[:, :, 0]
            V31 = tbs[:, :, 1]
            H50 = tbs[:, :, 2]
            V89 = tbs[:, :, 15]
            H165 = tbs[:, :, 16]
            H183 = tbs[:, :, 18]  # to match the 183+-4.5 GHz channel used by FNMOC

        # make dict of numpy arrays
        ingested = {
            "V23": V23,
            "V31": V31,
            "H50": H50,
            "V89": V89,
            "H165": H165,
            "H183": H183,
            "sdr_time": time_scan,
        }

    if "ATMS-SDR-GEO_All" in fileobj["All_Data"].keys():  # for geo-data
        data_select = fileobj["All_Data"]["ATMS-SDR-GEO_All"]

        # We will always read in latitude regardless if metadata_only is True.
        # Do this so we can filter out bad data, which can cause the start time
        # to be somewhere around 1957....
        lat = data_select["Latitude"][()]
        StartTime = data_select["StartTime"][()]
        #  get UTC time in datetime64 format required by geoips for each pixel
        time_scan = convert_epoch_to_datetime64(StartTime, use_shape=lat.shape)

        ingested = {
            "latitude": lat,
            "geo_time": time_scan,
            "valid_indices": ~(abs(lat) > 90),
        }
        if not metadata_only:
            ingested["longitude"] = data_select["Longitude"][()]
            ingested["solar_zenith_angle"] = data_select["SolarZenithAngle"][()]
            ingested["solar_azimuth_angle"] = data_select["SolarAzimuthAngle"][()]
            ingested["satellite_zenith_angle"] = data_select["SatelliteZenithAngle"][()]
            ingested["satellite_azimuth_angle"] = data_select["SatelliteAzimuthAngle"][
                ()
            ]

    platform_name = fileobj.attrs["Platform_Short_Name"][0, 0].decode("utf-8")

    # close the h5 object
    fileobj.close()
    # final_xarray = xr.Dataset()
    final_xarray = xarray_atms
    #          ------  setup xarray variables   ------
    for key, data in ingested.items():
        if key not in xarray_atms.variables.keys():
            final_xarray[key] = xr.DataArray(data)
        else:
            merged_array = np.vstack([xarray_atms[key], data])
            final_xarray[key] = xr.DataArray(
                merged_array, dims=["dim_" + str(merged_array.shape[0]), "dim_1"]
            )
    # Set official time to either sdr_time or geo_time
    final_keys = final_xarray.variables.keys()
    if "sdr_time" in final_keys:
        final_xarray["time"] = final_xarray["sdr_time"]
    else:
        final_xarray["time"] = final_xarray["geo_time"]

    # Map platform names found in data file attributes to consistent
    # GeoIPS naming conventions (match VIIRS reader).
    if platform_name == "J01":
        platform_name = "noaa-20"
    elif platform_name == "J02":
        platform_name = "noaa-21"
    elif platform_name == "NPP":
        platform_name = "npp"
    final_xarray.attrs["platform_name"] = platform_name
    final_xarray.attrs["data_provider"] = "NOAA"

    return final_xarray


def call(fnames, metadata_only=False, chans=None, area_def=None, self_register=False):
    """Read ATMS hdf5 data products.

    Parameters
    ----------
    fnames : list
        * List of strings, full paths to files
    metadata_only : bool, default=False
        * NOT YET IMPLEMENTED
        * Return before actually reading data if True
    chans : list of str, default=None
        * NOT YET IMPLEMENTED
        * List of desired channels (skip unneeded variables as needed).
        * Include all channels if None.
    area_def : pyresample.AreaDefinition, default=None
        * NOT YET IMPLEMENTED
        * Specify region to read
        * Read all data if None.
    self_register : str or bool, default=False
        * NOT YET IMPLEMENTED
        * register all data to the specified dataset id (as specified in the
          return dictionary keys).
        * Read multiple resolutions of data if False.

    Returns
    -------
    dict of xarray.Datasets
        * dictionary of xarray.Dataset objects with required Variables and
          Attributes.
        * Dictionary keys can be any descriptive dataset ids.

    See Also
    --------
    :ref:`xarray_standards`
        Additional information regarding required attributes and variables
        for GeoIPS-formatted xarray Datasets.
    """
    LOG.info("Reading files %s", fnames)

    # if metadata_only is True:  # read-in datafiles first time if 'metadata_only= True'
    xarray_atms = xr.Dataset()
    source_file_names = []
    for fname in fnames:
        xarray_atms = read_atms_file(fname, xarray_atms, metadata_only=metadata_only)
        source_file_names += [basename(fname)]  # name of last file from input files
    xarray_atms.attrs["source_file_names"] = source_file_names

    # setup attributors
    from geoips.xarray_utils.time import (
        get_max_from_xarray_time,
        get_min_from_xarray_time,
    )

    if "valid_indices" in xarray_atms:
        xarray_atms = xarray_atms.where(xarray_atms["valid_indices"])

    xarray_atms.attrs["start_datetime"] = get_min_from_xarray_time(xarray_atms, "time")
    xarray_atms.attrs["end_datetime"] = get_max_from_xarray_time(xarray_atms, "time")
    xarray_atms.attrs["source_name"] = "atms"

    # MTIFs need to be "prettier" for PMW products, so 2km resolution for
    # final image
    xarray_atms.attrs["sample_distance_km"] = 2
    xarray_atms.attrs["interpolation_radius_of_influence"] = (
        30000  # could be tuned if needed
    )

    return {"METADATA": xarray_atms[[]], "ATMS": xarray_atms}
