import json
import numpy as np
import uproot
import math
import copy
import mplhep as mh
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional, Union, List, Dict

from NanoAODTnP.RPCGeometry.RPCGeomServ import get_segment, get_roll_name


class DataLoader:
    def __init__(
        self, 
        input_path: Path, 
        roll_blacklist_path: Optional[Path] = None,
        keys: list = [],
    ):
        self.input_path = input_path
        self.roll_blacklist = self.load_blacklist(roll_blacklist_path)
        self.keys = keys
        self.tree = self.load_tree()
        self.total = uproot.open(f'{self.input_path}:total').to_hist()
        self.passed = uproot.open(f'{self.input_path}:passed').to_hist()
        self.region = 'All'
        self.facecolors = ['#8EFFF9', '#00AEC9']
        self.edgecolors = ['#005F77', '#005F77']
        self.hatches = ['///', None]

    def load_blacklist(self, roll_blacklist_path: Optional[Path]) -> set:
        if roll_blacklist_path is None:
            return set()
        with open(roll_blacklist_path) as stream:
            return set(json.load(stream))

    def load_tree(self) -> dict:
        input_keys = self.keys + ['region', 'ring', 'station', 'sector', 'layer', 'subsector', 'roll', 'is_fiducial', 'is_matched']
        tree = uproot.open(f'{self.input_path}:tree').arrays(input_keys, library='np')
        tree['roll_name'] = np.array([
            get_roll_name(tree['region'][i], tree['ring'][i], tree['station'][i],
                          tree['sector'][i], tree['layer'][i], tree['subsector'][i], tree['roll'][i])
            for i in range(len(tree['region']))
        ])
        self.keys = self.keys + ['is_fiducial', 'is_matched', 'roll_name']
        for id_key in ['region', 'ring', 'station', 'sector', 'layer', 'subsector', 'roll']:
            tree.pop(id_key)
        return tree

    def get_mask(self, key: str) -> np.ndarray:
        mask = True
        if key == 'is_fiducial':
            mask = self.tree['is_fiducial']
        if key == 'is_matched':
            mask = self.tree['is_matched']
        if key == 'is_linked':
            mask = np.vectorize(lambda name: name not in self.roll_blacklist)(self.tree['roll_name'])
        return mask

    def region_params(self, region: str) -> dict:
        facecolor_table = {'All': ['#8EFFF9', '#00AEC9'],
                           'Barrel': ['#d3f5e4', '#21bf70'],
                           'Disk123': ['#7CA1FF', '#0714FF'],
                           'Disk4': ['#FF6666', '#FF3300']}

        edgecolor_table = {'All': ['#005F77', '#005F77'],
                           'Barrel': ['#007700', '#007700'],
                           'Disk123': ['#000775', '#000775'],
                           'Disk4': ['#CC0000', '#CC0000']}

        hatches = ['///', None]
        is_region = np.vectorize(lambda item: item.startswith(region))
        facecolors = facecolor_table['All']
        edgecolors = edgecolor_table['All']

        if region == 'All':
            facecolors = facecolor_table[region]
            edgecolors = edgecolor_table[region]
            is_region = np.vectorize(lambda item: type(item) is str)
        elif region == 'Barrel':
            facecolors = facecolor_table[region]
            edgecolors = edgecolor_table[region]
            is_region = np.vectorize(lambda item: item.startswith('W'))
        elif region == 'Disk123':
            facecolors = facecolor_table[region]
            edgecolors = edgecolor_table[region]
            is_region = np.vectorize(lambda item: item.startswith(('RE+1', 'RE+2', 'RE+3', 'RE-1', 'RE-2', 'RE-3')))
        elif region == 'Disk4':
            facecolors = facecolor_table[region]
            edgecolors = edgecolor_table[region]
            is_region = np.vectorize(lambda item: item.startswith(('RE+4', 'RE-4')))
        elif region.startswith('W'):
            facecolors = facecolor_table['Barrel']
            edgecolors = edgecolor_table['Barrel']
        elif region.startswith(('RE+1', 'RE+2', 'RE+3', 'RE-1', 'RE-2', 'RE-3')):
            facecolors = facecolor_table['Disk123']
            edgecolors = edgecolor_table['Disk123']
        elif region.startswith(('RE+4', 'RE-4')):
            facecolors = facecolor_table['Disk4']
            edgecolors = edgecolor_table['Disk4']

        return {
            'is_region': is_region,
            'facecolors': facecolors,
            'edgecolors': edgecolors,
            'hatches': hatches
        }

    def filter_tree(self, keys: Union[str, list], region='All') -> dict:
        mask = None
        if type(keys) is str:
            mask = self.get_mask(keys)
        elif type(keys) is list:
            for key in keys:
                if mask is None:
                    mask = self.get_mask(key)
                mask = mask & self.get_mask(key)
        
        mask = mask & self.region_params(region)['is_region'](self.tree['roll_name'])

        filtered_data = copy.deepcopy(self)
        filtered_data.tree = {key: values[mask] for key, values in self.tree.items()}
        filtered_data.region = region
        filtered_data.facecolors = self.region_params(region)['facecolors']
        filtered_data.edgecolors = self.region_params(region)['edgecolors']
        filtered_data.hatches = self.region_params(region)['hatches']
        return filtered_data
