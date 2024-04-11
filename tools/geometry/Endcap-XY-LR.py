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

output_dir = Path.cwd() / source / 'XY-LR'
if not output_dir.exists():
    output_dir.mkdir(parents=True)

for station in stations:
    fig, ax = plt.subplots(figsize=(plotting_size*20, plotting_size*20))
    station_geometry = geometry[geometry['roll_name'].str.startswith(station)]
    for i in range(0, station_geometry.shape[0]):
        chamber = station_geometry.iloc[i]
        center_x = (chamber.x1 + chamber.x2 + chamber.x3 + chamber.x4) / 4
        center_y = (chamber.y1 + chamber.y2 + chamber.y3 + chamber.y4) / 4

        p1_p2_x = np.linspace((chamber.x1*9 + center_x)/10, (chamber.x2*9 + center_x)/10, 10)
        p1_p2_y = np.linspace((chamber.y1*9 + center_y)/10, (chamber.y2*9 + center_y)/10, 10)

        p2_p3_x = np.linspace((chamber.x2*9 + center_x)/10, (chamber.x3*9 + center_x)/10, 10)
        p2_p3_y = np.linspace((chamber.y2*9 + center_y)/10, (chamber.y3*9 + center_y)/10, 10)

        p3_p4_x = np.linspace((chamber.x3*9 + center_x)/10, (chamber.x4*9 + center_x)/10, 10)
        p3_p4_y = np.linspace((chamber.y3*9 + center_y)/10, (chamber.y4*9 + center_y)/10, 10)

        p4_p1_x = np.linspace((chamber.x4*9 + center_x)/10, (chamber.x1*9 + center_x)/10, 10)
        p4_p1_y = np.linspace((chamber.y4*9 + center_y)/10, (chamber.y1*9 + center_y)/10, 10)

        p_x = np.concatenate((p1_p2_x, p2_p3_x, p3_p4_x, p4_p1_x))
        p_y = np.concatenate((p1_p2_y, p2_p3_y, p3_p4_y, p4_p1_y))

        endcap_chamber_name = chamber.roll_name.split('_') # [RE+3, R3, CH29, A]
        if endcap_chamber_name[1][1] == "1":
            ax.text(center_x, center_y,
                    f'{endcap_chamber_name[1][-1]}/{endcap_chamber_name[2][2:]}/{endcap_chamber_name[3]}', # 3/29
                    fontsize=plotting_size*8,
                    va='center', ha='center')
        else:        
            ax.text(center_x, center_y,
                    f'{endcap_chamber_name[1][-1]}/{endcap_chamber_name[2][2:]}/{endcap_chamber_name[3]}', # 3/29
                    fontsize=plotting_size*10,
                    va='center', ha='center')

        ax.plot(p1_p2_x, p1_p2_y, c='black')
        ax.plot(p2_p3_x, p2_p3_y, c='red')
        ax.plot(p3_p4_x, p3_p4_y, c='black')
        ax.plot(p4_p1_x, p4_p1_y, c='blue')

    plt.plot([], [], c='red', label='p2-p3')
    plt.plot([], [], c='blue', label='p4-p1')
    ax.legend(fontsize=plotting_size*20, loc='upper right')
    ax.set_title(f'{station} RPC Geometry(from CMSSW)', fontsize=plotting_size*30)
    ax.set_xlabel('axis-X', fontsize=plotting_size*20)
    ax.set_ylabel('axis-Y', fontsize=plotting_size*20)

    ax.add_artist(offsetbox.AnchoredText(f'Source: {source}',
                                         loc='upper left',
                                         prop=dict(size=plotting_size*20)))
    output_path = output_dir / station
    plt.savefig(output_path.with_suffix('.png'))