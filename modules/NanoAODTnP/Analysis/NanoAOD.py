from typing import Optional
from pathlib import Path
import numpy as np
import awkward as ak
import uproot
import pandas as pd
from hist.hist import Hist
from hist.axis import StrCategory, IntCategory
import json

from NanoAODTnP.RPCGeometry.RPCGeomServ import get_roll_name
from NanoAODTnP.Analysis.LumiBlockChecker import LumiBlockChecker

def get_blacklist_mask(arr_var: np.ndarray,
                       blacklist_path: str,
):
    if blacklist_path is None:
        blacklist = set()
    with open(blacklist_path) as stream:
        blacklist = set(json.load(stream))

    blacklist_mask = np.vectorize(lambda var: var not in blacklist)(arr_var)
    return blacklist_mask

def read_nanoaod(path,
                 cert_path: str,
                 treepath: str = 'Events',
                 name: str = 'rpcTnP',
):
    tree = uproot.open(f'{path}:{treepath}')

    aliases = {key.removeprefix(f'{name}_'): key
               for key in tree.keys()
               if key.startswith(name)}
    # number of measurements
    aliases['size'] = f'n{name}'
    expressions = list(aliases.keys()) + ['run', 'luminosityBlock', 'event']
    cut = f'(n{name} > 0)'

    data: dict[str, np.ndarray] = tree.arrays(
        expressions = expressions,
        aliases = aliases,
        cut = cut,
        library = 'np'
    )

    run = data.pop('run')
    lumi_block = data.pop('luminosityBlock')
    size = data.pop('size')
    event = data.pop('event')


    lumi_block_checker = LumiBlockChecker.from_json(cert_path)
    mask = lumi_block_checker.get_lumi_mask(run, lumi_block)
    data = {key: value[mask] for key, value in data.items()}

    data = {key: np.concatenate(value) for key, value in data.items()}
    data['run'] = np.repeat(run[mask], size[mask])
    data['event'] = np.repeat(event[mask], size[mask])

    return data

def flatten_nanoaod(input_path: Path,
                    cert_path: Path,
                    geom_path: Path,
                    output_path: Path,
                    roll_blacklist_path: Optional[str] = None,
                    run_blacklist_path: Optional[str] = None,
                    name: str = 'rpcTnP',
):
    data = read_nanoaod(
        path = input_path,
        cert_path = cert_path,
        treepath = 'Events',
        name = name
    )
    data['roll_name'] = np.array([
        get_roll_name(data['region'][i], data['ring'][i], data['station'][i],
                      data['sector'][i], data['layer'][i], data['subsector'][i], 
                      data['roll'][i])
        for i in range(len(data['region']))
    ])

    mask = np.ones(data['roll_name'].shape, dtype=bool)

    if run_blacklist_path is not None:
        mask = mask & get_blacklist_mask(
            arr_var = data['run'],
            blacklist_path = run_blacklist_path,
        )
    if roll_blacklist_path is not None:
        mask = mask & get_blacklist_mask(
            arr_var = data['roll_name'],
            blacklist_path = roll_blacklist_path,
        )
    
    data = {key: value[mask] for key, value in data.items()}

    geom = pd.read_csv(geom_path)
    roll_axis = StrCategory(geom['roll_name'].tolist())
    
    h_total_by_roll = Hist(roll_axis) # type: ignore
    h_passed_by_roll = h_total_by_roll.copy()
    h_total_by_roll.fill(data['roll_name'][data['is_fiducial']])
    h_passed_by_roll.fill(data['roll_name'][data['is_fiducial'] & data['is_matched']])

    run_axis = IntCategory(np.unique(data['run']))
    h_total_by_run = Hist(run_axis)
    h_passed_by_run = h_total_by_run.copy()
    h_total_by_run.fill(data['run'][data['is_fiducial']])
    h_passed_by_run.fill(data['run'][data['is_fiducial'] & data['is_matched']])

    roll_name = data.pop('roll_name')
    data = ak.Array(data)
    with uproot.writing.create(output_path) as output_file:
        output_file['tree'] = data
        output_file['total_by_roll'] = h_total_by_roll
        output_file['passed_by_roll'] = h_passed_by_roll
        output_file['total_by_run'] = h_total_by_run
        output_file['passed_by_run'] = h_passed_by_run
