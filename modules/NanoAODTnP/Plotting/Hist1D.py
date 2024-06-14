import json
import numpy as np
import pandas as pd
import uproot
import mplhep as mh
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional, Union
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle

from NanoAODTnP.RPCGeometry.RPCGeomServ import get_segment, get_roll_name
from NanoAODTnP.Plotting.DataLoader import DataLoader

def init_figure(
    figsize: tuple = (8, 6),
    fontsize: float = 20,
    com: float = 13.6,
    label1: str = 'Work in Progress',
    label2: Optional[str] = None,
    loc: int = 2,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    xlim: Optional[tuple] = None,
    ylim: Optional[tuple] = None,
    xticks: Optional[list] = None,
    yticks: Optional[list] = None,
    log_scale: bool = False,
) -> plt.Figure:
    mh.style.use(mh.styles.CMS)
    fig, ax = plt.subplots(figsize = figsize)
    mh.cms.label(ax = ax, data = True, label = label1, loc = loc,
                 year = label2, com = com, fontsize = fontsize)
    ax.set_xlabel(xlabel, fontsize = fontsize)
    ax.set_ylabel(ylabel, fontsize = fontsize)
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:    
        ax.set_ylim(ylim)
    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)
    if log_scale == True:
        ax.set_yscale(log)
    return fig, ax

def eff_hist(data1, data2, output_path):
    eff1 = np.divide(
        data1.passed, data1.total,
        out = np.zeros_like(data1.total),
        where = (data1.total > 0)
    ) * 100

    eff2 = np.divide(
        data2.passed, data2.total,
        out = np.zeros_like(data2.total),
        where = (data2.total > 0)
    ) * 100

    fig, ax = init_figure(
        figsize = (12, 8),
        fontsize = 24,
        com = 13.6,
        label1 = 'Work in Progress',
        label2 = f'{data1.region}',
        loc = 0,
        xlabel = 'Efficiency [%]',
        ylabel = 'Number of Rolls',
        xlim = (70, 100),
        ylim = None,
        xticks = None,
        yticks = None,
        log_scale = False,
    )

    count1, bins1, patch1 = ax.hist(
        eff1, 
        bins = 101, 
        range = (0, 101),
        facecolor = data1.facecolors[0],
        edgecolor = data1.edgecolors[0],
        hatch = data1.hatches[0],
        alpha = 0.5,
        align = 'mid',
        density = False,
        linewidth = 1.6,
        histtype = 'stepfilled',
    )

    count2, bins2, patch2 = ax.hist(
        eff2, 
        bins = 101, 
        range = (0, 101),
        facecolor = data2.facecolors[1],
        edgecolor = data2.edgecolors[1],
        hatch = data2.hatches[1],
        alpha = 0.5,
        align = 'mid',
        density = False,
        linewidth = 1.6,
        histtype = 'stepfilled',
    )
    
    extra = Rectangle((0, 0), 0.1, 0.1, fc='w', fill=False, edgecolor='none', linewidth=0)
    header_row = ['', 'Data', 'Mean', 'Mean(>70%)', 'Entries', 'Underflow']
    data1_row = [
        '', 
        'Run2022', 
        f'{np.mean(eff1) : .2f}', 
        f'{np.mean(eff1[eff1 > 70]) : .2f}',
        f'{len(eff1)}',
        f'{len(eff1[eff1 <= 70])}',
    ]
    data2_row = [
        '', 
        'Run2023', 
        f'{np.mean(eff2) : .2f}', 
        f'{np.mean(eff2[eff2 > 70]) : .2f}',
        f'{len(eff2)}',
        f'{len(eff2[eff2 <= 70])}',
    ]
    legend_handles, legend_values = [], []
    for idx in range(len(header_row)):
        if idx == 0:
            legend_handles += [extra, patch1[0], patch2[0]]
        else:
            legend_handles += [extra, extra, extra]
        legend_values += [header_row[idx], data1_row[idx], data2_row[idx]]

    ax.legend(
        legend_handles, legend_values,
        ncol = len(header_row), columnspacing = 0.0,
        handletextpad = 0.0, handlelength = 1.0,
        alignment = 'center', loc = 'upper left',
        fontsize = 20,
    )
    output_path = Path(output_path)
    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True)
    fig.savefig(output_path)
    return [eff1, eff2]
