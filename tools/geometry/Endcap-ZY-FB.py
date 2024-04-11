import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.offsetbox as offsetbox
from matplotlib.animation import FuncAnimation
from pathlib import Path
import argparse


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-s', '--source', type=str, help='geometry source', default='rpcf_2024_v2')
args = parser.parse_args()
source = args.source

geom_path = (Path(__file__).parents[0] / 'csv' / source).with_suffix('.csv')
geometry = pd.read_csv(geom_path, sep=',', index_col=False)
stations = ['RE-1', 'RE-2', 'RE-3', 'RE-4', 'RE+1', 'RE+2', 'RE+3', 'RE+4']
plotting_size = 1.6

output_dir = Path.cwd() / source / 'ZY-FB'
if not output_dir.exists():
    output_dir.mkdir(parents=True)

for station in stations:
    fig, ax = plt.subplots(figsize=(plotting_size*20, plotting_size*20))
    station_geometry = geometry[geometry['roll_name'].str.startswith(station)]
    station_mean_z = station_geometry.mean(numeric_only=True).z1 

    unique_z = station_geometry.z1.unique()

    for z in np.sort(unique_z):
        z_geometry = station_geometry[station_geometry.z1 == z]
        y_all = np.concatenate([z_geometry.y1, z_geometry.y2, z_geometry.y3, z_geometry.y4])
        y_min = y_all.min()
        y_max = y_all.max()
        is_front = z_geometry.is_front.unique()
        if not len(is_front) == 1:
            print("front back problem")
            break
        
        if is_front == True:
            plt.plot([z, z], [y_min, y_max], c='red', label=f'front chamber, z={z}', linewidth=plotting_size*5)
        if is_front == False:
            plt.plot([z, z], [y_min, y_max], c='blue', label=f'back chamber, z={z}', linewidth=plotting_size*5)

    
    ax.set_xlim(station_mean_z - 30, station_mean_z + 30)
    ax.set_xlabel('axis-Z', fontsize=plotting_size*20)
    ax.set_ylabel('axis-Y', fontsize=plotting_size*20)

    ax.set_title(f'{station} RPC Geometry(from CMSSW)', fontsize=plotting_size*30)

    ax.add_artist(offsetbox.AnchoredText(f'Source: {source}',
                                         loc='upper left',
                                         prop=dict(size=plotting_size*20)))

    ax.legend(fontsize=plotting_size*20, loc='upper right')

    output_path = output_dir / station
    plt.savefig(output_path.with_suffix('.png'))


    