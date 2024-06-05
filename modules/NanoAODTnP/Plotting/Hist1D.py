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
    fig, ax = plt.subplots(figsize = (16, 10))
    mh.cms.label(ax = ax, data = True, label = label1, loc = loc,
                 year = label2, com = com, fontsize = 30)
    ax.set_xlabel(xlabel, fontsize=24)
    ax.set_ylabel(ylabel, fontsize=24)
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

def hist1d(
    ax: plt.Axes,
    input_data: np.ndarray,
    h_bins: int,
    h_range: tuple,
    facecolor: str = '#00AEC9',
    edgecolor: str = '#005F77',
    hatch: Optional[str] = None,
    alpha: float = 1.0,
    align: str = 'left',
    density: bool = False,
):
    count, bins, patch = ax.hist(
        input_data, 
        bins = h_bins, 
        range = h_range,
        facecolor = facecolor,
        edgecolor = edgecolor,
        hatch = hatch,
        alpha = alpha,
        align = align,
        density = density,
        linewidth = 1.6,
        histtype = 'stepfilled',
    )
    return ax, patch
