"""Generic satpy reader"""

import logging
from typing import Any, Dict, List, Optional, Union

import pyresample.geometry
import satpy
import xarray as xr

log = logging.getLogger(__name__)

interface = "readers"
family = "standard"
name = "generic_satpy"


def call(
    fnames: List[str],
    start_time_meta_path: str,
    end_time_meta_path: str,
    source_name: str,
    platform_name: str,
    metadata_only: bool = False,
    chans: Optional[List[str]] = None,
    area_def: Optional[pyresample.geometry.AreaDefinition] = None,
    self_register: bool = False,
    satpy_reader: str = "ahi_hsd",
    channel_groups: Dict[str, List[str]] = {"0.5km": ["B09"]},
    roi: float = 3000,
    filter_parameters: Optional[Dict[str, Any]] = None,
    satpy_reader_kwargs: Optional[Dict[str, Any]] = None,
    calibration: Union[List[str], str] = "*",
    resolution: Union[List[float], float] = "*",
    polarization: Union[List[str], str] = "*",
    level: Union[List[float], str] = "*",
    modifiers: Union[List[str], str] = "*",
    generate: bool = True,
    unload: bool = True,
    load_kwargs: Optional[Dict[str, Any]] = None,
    force_compute: bool = False,
) -> Dict[str, xr.DataArray]:
    if platform_name is None:
        platform_name = satpy_reader

    scene = satpy.Scene(
        filenames=fnames,
        reader=satpy_reader,
        filter_parameters=filter_parameters,
        reader_kwargs=satpy_reader_kwargs,
    )

    all_channels = []
    for channel_names in channel_groups.values():
        all_channels.extend(channel_names)

    if load_kwargs is None:
        load_kwargs = {}

    scene.load(
        all_channels,
        calibration=calibration,
        resolution=resolution,
        polarization=polarization,
        level=level,
        modifiers=modifiers,
        generate=generate,
        unload=unload,
        **load_kwargs
    )

    output_datasets = {}
    for group_name, channel_names in channel_groups.items():
        lons, lats, start_time, end_time = (None, None, None, None)
        is_first_channel = True
        data_dict = {}
        for channel_name in channel_names:
            channel = scene[channel_name]
            if is_first_channel:
                lons_np, lats_np = channel.attrs["area"].get_lonlats()
                lons = xr.DataArray(lons_np, dims={"y": channel.y, "x": channel.x})
                lats = xr.DataArray(lats_np, dims={"y": channel.y, "x": channel.x})

                start_time = _get_metadata_entry_from_string(
                    start_time_meta_path, channel.attrs
                )
                end_time = _get_metadata_entry_from_string(
                    end_time_meta_path, channel.attrs
                )

            if force_compute and not metadata_only:
                channel.data = channel.data.compute()

            data_dict[channel_name] = channel

        data_dict["longitude"] = lons
        data_dict["latitude"] = lats

        group_dataset = xr.Dataset(data_dict)
        group_dataset.attrs["source_name"] = source_name
        group_dataset.attrs["platform_name"] = platform_name
        group_dataset.attrs["data_provider"] = "satpy"
        group_dataset.attrs["start_datetime"] = start_time
        group_dataset.attrs["end_datetime"] = end_time
        group_dataset.attrs["interpolation_radius_of_influence"] = roi

        output_datasets[group_name] = group_dataset
        output_datasets["METADATA"] = group_dataset[[]]

    return output_datasets


def _get_metadata_entry_from_string(metadata_path: str, attrs: Dict[str, Any]) -> Any:
    split_path = metadata_path.split("/")
    current_attr_level = attrs
    for path_entry in split_path:
        current_attr_level = current_attr_level[path_entry]

    return current_attr_level
