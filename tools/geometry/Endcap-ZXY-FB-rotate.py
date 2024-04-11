import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.offsetbox as offsetbox
from matplotlib.animation import FuncAnimation
from pathlib import Path
import argparse


def update(frame_number):
    ax.view_init(azim=225 + frame_number*2)


parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-s', '--source', type=str, help='geometry source', default='rpcf_2024_v2')
args = parser.parse_args()
source = args.source

geom_path = (Path(__file__).parents[0] / 'csv' / source).with_suffix('.csv')
geometry = pd.read_csv(geom_path, sep=',', index_col=False)
stations = ['RE-1', 'RE-2', 'RE-3', 'RE-4', 'RE+1', 'RE+2', 'RE+3', 'RE+4']
plotting_size = 1.6

output_dir = Path.cwd() / source / 'XYZ-FB'
if not output_dir.exists():
    output_dir.mkdir(parents=True)

for station in stations:
    fig, ax = plt.subplots(figsize=(plotting_size*8, plotting_size*8), subplot_kw={"projection": "3d"})
    station_geometry = geometry[geometry['roll_name'].str.startswith(station)]
    station_mean_z = station_geometry.mean(numeric_only=True).z1 
    for i in range(0, station_geometry.shape[0]):
        chamber = station_geometry.iloc[i]
        center_x = (chamber.x1 + chamber.x2 + chamber.x3 + chamber.x4) / 4
        center_y = (chamber.y1 + chamber.y2 + chamber.y3 + chamber.y4) / 4
        center_z = (chamber.z1 + chamber.z2 + chamber.z3 + chamber.z4) / 4
        p1_p2_x = np.linspace((chamber.x1*9 + center_x)/10, (chamber.x2*9 + center_x)/10, 10)
        p1_p2_y = np.linspace((chamber.y1*9 + center_y)/10, (chamber.y2*9 + center_y)/10, 10)
        p1_p2_z = np.linspace((chamber.z1*9 + center_z)/10, (chamber.z2*9 + center_z)/10, 10)
        p2_p3_x = np.linspace((chamber.x2*9 + center_x)/10, (chamber.x3*9 + center_x)/10, 10)
        p2_p3_y = np.linspace((chamber.y2*9 + center_y)/10, (chamber.y3*9 + center_y)/10, 10)
        p2_p3_z = np.linspace((chamber.z2*9 + center_z)/10, (chamber.z3*9 + center_z)/10, 10)
        p3_p4_x = np.linspace((chamber.x3*9 + center_x)/10, (chamber.x4*9 + center_x)/10, 10)
        p3_p4_y = np.linspace((chamber.y3*9 + center_y)/10, (chamber.y4*9 + center_y)/10, 10)
        p3_p4_z = np.linspace((chamber.z3*9 + center_z)/10, (chamber.z4*9 + center_z)/10, 10)
        p4_p1_x = np.linspace((chamber.x4*9 + center_x)/10, (chamber.x1*9 + center_x)/10, 10)
        p4_p1_y = np.linspace((chamber.y4*9 + center_y)/10, (chamber.y1*9 + center_y)/10, 10)
        p4_p1_z = np.linspace((chamber.z4*9 + center_z)/10, (chamber.z1*9 + center_z)/10, 10)
        p_x = np.concatenate((p1_p2_x, p2_p3_x, p3_p4_x, p4_p1_x))
        p_y = np.concatenate((p1_p2_y, p2_p3_y, p3_p4_y, p4_p1_y))
        p_z = np.concatenate((p1_p2_z, p2_p3_z, p3_p4_z, p4_p1_z))
        if chamber.is_front == True:
            ax.plot(p_z, p_x, p_y, c="red")
        if chamber.is_front == False:
            ax.plot(p_z, p_x, p_y, c="blue")
    ax.set_xlim(station_mean_z - 30, station_mean_z + 30)
    plt.plot([], [], c='red', label='front chamber')
    plt.plot([], [], c='blue', label='back chamber')
    ax.set_title(f'{station} RPC Geometry(from CMSSW)', fontsize=plotting_size*16)
    ax.legend(fontsize=plotting_size*12, loc='upper right')
    ax.set_xlabel('axis-Z', fontsize=plotting_size*12)
    ax.set_ylabel('axis-X', fontsize=plotting_size*12)
    ax.set_zlabel('axis-Y', fontsize=plotting_size*12)
    ax.view_init(elev=20, azim=225)
    ax.add_artist(offsetbox.AnchoredText(f'Source: {source}',
                                         loc='upper left',
                                         prop=dict(size=plotting_size*10)))
    anim = FuncAnimation(fig, update, frames=180, interval=200)
    output_path = output_dir / station
    anim.save(output_path.with_suffix('.gif'), fps=10)
    