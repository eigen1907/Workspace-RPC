from typing import Optional
from pathlib import Path
import numpy as np
import awkward as ak
import uproot
import pandas as pd
from hist.hist import Hist
from hist.axis import StrCategory

from NanoAODTnP.RPCGeometry.RPCGeomServ import get_roll_name
from NanoAODTnP.Analysis.LumiBlockChecker import LumiBlockChecker


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
        expressions=expressions,
        aliases=aliases,
        cut=cut,
        library='np'
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

    return ak.Array(data)


def flatten_nanoaod(input_path: Path,
                    cert_path: Path,
                    geom_path: Path,
                    output_path: Path,
                    name: str = 'rpcTnP',
):
    data = read_nanoaod(
        path=input_path,
        cert_path=cert_path,
        treepath='Events',
        name=name
    )

    name_arr = [get_roll_name(row.region, row.ring, row.station,
                              row.sector, row.layer, row.subsector,
                              row.roll)
                for row in data]
    name_arr = np.array(name_arr)

    geom = pd.read_csv(geom_path)

    roll_axis = StrCategory(geom['roll_name'].tolist())
    h_total = Hist(roll_axis) # type: ignore
    h_passed = h_total.copy()

    h_total.fill(name_arr[data.is_fiducial])
    h_passed.fill(name_arr[data.is_fiducial & data.is_matched].tolist())

    with uproot.writing.create(output_path) as output_file:
        output_file['tree'] = data
        output_file['total'] = h_total
        output_file['passed'] = h_passed
