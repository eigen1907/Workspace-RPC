import json
import numpy as np
import pandas as pd
import uproot
import mplhep as mh
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional, Union
from matplotlib.colors import LogNorm

from NanoAODTnP.RPCGeometry.RPCGeomServ import get_segment, get_roll_name


def load_tree(
    input_path: Path,
    columns: list,
    roll_blacklist_path: Optional[Path] = None,
) -> dict:
    ######################################################################################
    ##     COLUMNS
    ##     'is_fiducial', 'is_matched', 
    ##     'region', 'ring', 'station', 'sector', 'layer', 'subsector', 'roll', 
    ##     'run', 'cls', 'bx', 'event',
    ##     'tag_pt', 'tag_eta', 'tag_phi', 
    ##     'probe_pt', 'probe_eta', 'probe_phi', 'probe_time', 'probe_dxdz', 'probe_dydz', 
    ##     'dimuon_pt', 'dimuon_mass', 
    ##     'residual_x', 'residual_y', 'pull_x', 'pull_y', 'pull_x_v2', 'pull_y_v2', 
    ######################################################################################
    data = uproot.open(f"{str(input_path)}:tree").arrays(columns, library='np')
    
    fiducial_mask = data['is_fiducial']
    for key, values in data.items():
        data[key] = data[key][fiducial_mask]

    data['roll_name'] = np.array([
        get_roll_name(
            data['region'][idx], data['ring'][idx], data['station'][idx],
            data['sector'][idx], data['layer'][idx], data['subsector'][idx], data['roll'][idx]
        ) for idx in range(len(data['region']))
    ])

    if roll_blacklist_path is None:
        roll_blacklist = set()
    else:
        with open(roll_blacklist_path) as stream:
            roll_blacklist = set(json.load(stream))
    
    is_blacklist = np.vectorize(lambda item: item in roll_blacklist)
    blacklist_mask = is_blacklist(data['roll_name'])

    for key, values in data.items():
        data[key] = data[key][~blacklist_mask]

    return data


def filter_by_region(
    data: dict,
    region: str
):
    if region == "all":
        is_region = np.vectorize(lambda item: type(item) is str)
    elif region == "barrel":
        is_region = np.vectorize(lambda item: item.startswith('W'))
    elif region == "disk123":
        is_region = np.vectorize(lambda item: item.startswith(('RE+1', 'RE+2', 'RE+3', 'RE-1', 'RE-2', 'RE-3')))
    elif region == "disk4":
        is_region = np.vectorize(lambda item: item.startswith(('RE+4', 'RE-4')))
    else:
        is_region = np.vectorize(lambda item: item.startswith(region))
        
    region_mask = is_region(data['roll_name'])
    region_data = {}
    for key, values in data.items():
        region_data[key] = data[key][region_mask]

    return region_data