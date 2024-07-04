import json
import uproot
import numpy as np
import pandas as pd
import mplhep as mh

from pathlib import Path
from typing import Optional, Union
from hist import intervals
from datetime import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle

def init_figure(
    figsize: tuple = (8, 6),
    fontsize: float = 20,
    com: float = 13.6,
    label1: str = 'Work in Progress',
    label2: Optional[str] = None,
    mid_label: Optional[str] = None,
    loc: int = 2,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    xlim: Optional[tuple] = None,
    ylim: Optional[tuple] = None,
    xticks: Optional[list] = None,
    yticks: Optional[list] = None,
    log_scale: bool = False,
) -> plt.Figure:
    #mh.style.use(mh.styles.CMS)
    fig, ax = plt.subplots(figsize = figsize)
    mh.cms.label(ax = ax, data = True, label = label1, loc = loc,
                 year = label2, com = com, fontsize = fontsize)
    ax.set_xlabel(xlabel, fontsize = fontsize)
    ax.set_ylabel(ylabel, fontsize = fontsize)
    if mid_label is not None:
        ax.annotate(mid_label, (0.50, 1.015), #weight='bold',
                    xycoords='axes fraction', fontsize=fontsize, horizontalalignment='center')
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

def get_region_params(region: str) -> dict:
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
    elif region == 'Endcap':
        facecolors = facecolor_table['Disk123']
        edgecolors = edgecolor_table['Disk123']
        is_region = np.vectorize(lambda item: item.startswith('RE'))
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

def hist_eff_by_roll(input_path_1, input_path_2, region, output_path):
    total_by_roll_1 = uproot.open(f'{input_path_1}:total_by_roll').to_hist()
    passed_by_roll_1 = uproot.open(f'{input_path_1}:passed_by_roll').to_hist()

    total_by_roll_2 = uproot.open(f'{input_path_2}:total_by_roll').to_hist()
    passed_by_roll_2 = uproot.open(f'{input_path_2}:passed_by_roll').to_hist()

    total_1 = total_by_roll_1.values()
    passed_1 = passed_by_roll_1.values()
    roll_name_1 = np.array(total_by_roll_1.axes[0])

    total_2 = total_by_roll_2.values()
    passed_2 = passed_by_roll_2.values()
    roll_name_2 = np.array(total_by_roll_2.axes[0])

    eff_1 = np.divide(passed_1, total_1,
                      out = np.zeros_like(total_1),
                      where = (total_1 > 0)) * 100

    eff_2 = np.divide(passed_2, total_2,
                      out = np.zeros_like(total_2),
                      where = (total_2 > 0)) * 100

    region_params = get_region_params(region)
    eff_1 = eff_1[region_params['is_region'](roll_name_1) & (total_1 != 0)]
    eff_2 = eff_2[region_params['is_region'](roll_name_2) & (total_2 != 0)]

    fig, ax = init_figure(
        figsize = (12, 8),
        fontsize = 24,
        com = 13.6,
        label1 = 'Work in Progress',
        label2 = f'{region}',
        loc = 0,
        xlabel = 'Efficiency [%]',
        ylabel = 'Number of Rolls',
        xlim = (70, 100),
        ylim = None,
        xticks = None,
        yticks = None,
        log_scale = False,
    )

    count_1, bins_1, patch_1 = ax.hist(eff_1[eff_1 > 0], 
                                       bins = 200, 
                                       range = (0, 100),
                                       facecolor = region_params['facecolors'][0],
                                       edgecolor = region_params['edgecolors'][0],
                                       hatch = region_params['hatches'][0],
                                       alpha = 0.5,
                                       align = 'mid',
                                       density = False,
                                       linewidth = 1.6,
                                       histtype = 'stepfilled')

    count_2, bins_2, patch_2 = ax.hist(eff_2[eff_2 > 0], 
                                       bins = 200,
                                       range = (0, 100),
                                       facecolor = region_params['facecolors'][1],
                                       edgecolor = region_params['edgecolors'][1],
                                       hatch = region_params['hatches'][1],
                                       alpha = 0.5,
                                       align = 'mid',
                                       density = False,
                                       linewidth = 1.6,
                                       histtype = 'stepfilled')
    
    extra = Rectangle((0, 0), 0.1, 0.1, fc='w', fill=False, edgecolor='none', linewidth=0)
    header_row = ['',
                  '',
                  r'$\mu_{eff}$',
                  r'$\mu_{eff>70 \%}$',
                  r'$N_{total}$',
                  r'$N_{eff<70 \%}$',
                  r'$N_{excluded}$',]

    n_total_1 = len(total_1[region_params['is_region'](roll_name_1)])
    n_eff_under_70_1 = len(eff_1[eff_1 <= 70])
    n_excluded_1 = len(total_1[region_params['is_region'](roll_name_1) & (total_1 == 0)])

    data_1_row = ['', 
                  '2022', 
                  f'{np.mean(eff_1):.1f} %', 
                  f'{np.mean(eff_1[eff_1 > 70]):.1f} %',
                  f'{n_total_1}',
                  f'{n_eff_under_70_1} ({n_eff_under_70_1/n_total_1*100:.1f} %)',
                  f'{n_excluded_1} ({n_excluded_1/n_total_1*100:.1f} %)',]
    
    n_total_2 = len(total_2[region_params['is_region'](roll_name_2)])
    n_eff_under_70_2 = len(eff_2[eff_2 <= 70])
    n_excluded_2 = len(total_2[region_params['is_region'](roll_name_2) & (total_2 == 0)])

    data_2_row = ['', 
                  '2023', 
                  f'{np.mean(eff_2):.1f} %', 
                  f'{np.mean(eff_2[eff_2 > 70]):.1f} %',
                  f'{n_total_2}',
                  f'{n_eff_under_70_2} ({n_eff_under_70_2/n_total_2*100:.1f} %)',
                  f'{n_excluded_2} ({n_excluded_2/n_total_2*100:.1f} %)',]

    legend_handles, legend_values = [], []
    for idx in range(len(header_row)):
        if idx == 0:
            legend_handles += [extra, patch_1[0], patch_2[0]]
        else:
            legend_handles += [extra, extra, extra]
        legend_values += [header_row[idx], data_1_row[idx], data_2_row[idx]]

    ax.legend(legend_handles, legend_values,
              ncol = len(header_row), columnspacing = 0.0,
              handletextpad = -0.6, handlelength = 1.5,
              alignment = 'center', loc = 'upper left', fontsize = 20)
    output_path = Path(output_path)
    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True)
    fig.savefig(output_path)
    plt.close(fig)
    return [eff_1, eff_2]

def run2time(run, run_info):
    time = None
    while True:
        if time is not None: break
        if round(run) in run_info['run_number'].values:
            time = run_info['start_time'][run_info['run_number'] == round(run)].values[0]
            time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        run += 1
    return time

def runs2times(runs, run_info):
    times = []
    for run in runs:
        time = run_info['start_time'][run_info['run_number'] == run].values[0]
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        times.append(time)
    return np.array(times)

def plot_eff_time(ax, input_path, run_info, region, fix_color=True, alpha=1.0):
    total_by_roll_run = uproot.open(f'{input_path}:total_by_roll_run').to_hist()
    passed_by_roll_run = uproot.open(f'{input_path}:passed_by_roll_run').to_hist()

    total = total_by_roll_run.values()
    passed = passed_by_roll_run.values()

    roll_name = np.array(total_by_roll_run.axes[0])
    runs = np.array(total_by_roll_run.axes[1])

    region_params = get_region_params(region)
    total = np.sum(total[region_params['is_region'](roll_name)], axis=0)
    passed = np.sum(passed[region_params['is_region'](roll_name)], axis=0)

    runs_mask = (total != 0)

    total = total[runs_mask]
    passed = passed[runs_mask]
    runs = runs[runs_mask]
    times = runs2times(runs, run_info)

    effs = np.divide(passed, total,
                    out = np.zeros_like(total),
                    where = (total > 0)) * 100

    errs = intervals.clopper_pearson_interval(passed, total, 0.68) * 100

    lower_limits = effs - errs[0]
    upper_limits = errs[1] - effs

    ax.errorbar(
        times,
        effs,
        yerr = (lower_limits, upper_limits),
        fmt = 's',
        markersize = 6,
        markerfacecolor = 'none',
        markeredgewidth = 2,
        lw = 2,
        capsize = 4,
        color = region_params['facecolors'][1] if fix_color is True else None,
        label = region,
        alpha = alpha,
    )
    return ax, effs, runs

def plot_eff_by_time_2022(input_path_2022, run_info_path, region, output_path, fix_color=True, alpha=1.0):
    if type(region) is list:
        mid_label = 'RPC Efficiency'
    elif type(region) is str:
        mid_label = f'RPC {region} Efficiency'
    fig, ax = init_figure(
        figsize = (20, 9),
        fontsize = 24,
        com = 13.6,
        label1 = 'Work in Progress',
        label2 = f'2022 Data',
        mid_label = f'{mid_label}',
        loc = 0,
        ylabel = 'Efficiency [%]',
        xlim = None,
        ylim = None,
        xticks = None,
        yticks = None,
        log_scale = False,
    )

    run_info = pd.read_csv(run_info_path, index_col = False)
    
    ymin, ymax = 0, 100
    ax.set_xlim(datetime.strptime('2022/01/Jul', '%Y/%d/%b'), datetime.strptime('2022/01/Dec', '%Y/%d/%b'))
    ax.set_ylim(ymin, ymax)
    
    if type(region) is list:
        for i_region in region:
            ax, effs, runs = plot_eff_time(ax, input_path_2022, run_info, i_region, fix_color, alpha)      
        ax.legend(loc='center right', fontsize = 28) 
    elif type(region) is str:
        ax, effs, runs = plot_eff_time(ax, input_path_2022, run_info, region, fix_color, alpha)
    
    spans = [
        (355100, 355769, 'Run2022B', 'y'),
        (355862, 357482, 'Run2022C', 'm'),
        (357538, 357900, 'Run2022D', 'y'),
        (359356, 360327, 'Run2022E', 'm'),
        (360335, 362167, 'Run2022F', 'y'),
        (362362, 362760, 'Run2022G', 'm'),
    ]
    
    for start, end, label, color in spans:
        ax.axvspan(run2time(start, run_info), run2time(end, run_info), color=color, alpha=0.1)
        mid_point = run2time((start + end) // 2, run_info)
        ax.text(mid_point, ymin + 15, label, rotation=90, verticalalignment='center', fontsize=22, weight='bold', color=color)
    
    #ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=(1, 15)))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    #ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%b'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
    ax.grid()
    
    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True)
    fig.savefig(output_path)
    plt.close(fig)

def plot_eff_by_time_2023(input_path_2023, run_info_path, region, output_path, fix_color=True, alpha=1.0):
    if type(region) is list:
        mid_label = 'RPC Efficiency'
    elif type(region) is str:
        mid_label = f'RPC {region} Efficiency'
    fig, ax = init_figure(
        figsize = (20, 9),
        fontsize = 24,
        com = 13.6,
        label1 = 'Work in Progress',
        label2 = f'2023 Data',
        mid_label = f'{mid_label}',
        loc = 0,
        ylabel = 'Efficiency [%]',
        xlim = None,
        ylim = None,
        xticks = None,
        yticks = None,
        log_scale = False,
    )
    run_info = pd.read_csv(run_info_path, index_col = False)

    ymin, ymax = 0, 100
    ax.set_xlim(datetime.strptime('2023/01/Apr', '%Y/%d/%b'), datetime.strptime('2023/01/Aug', '%Y/%d/%b'))
    ax.set_ylim(ymin, ymax)
    
    if type(region) is list:
        for i_region in region:
            ax, effs, runs = plot_eff_time(ax, input_path_2023, run_info, i_region, fix_color, alpha)     
        ax.legend(loc='center right', fontsize = 28) 
    elif type(region) is str:
        ax, effs, runs = plot_eff_time(ax, input_path_2023, run_info, region, fix_color, alpha)
    
    spans = [
        (366403, 367079, 'Run2023B', 'y'),
        (367770, 369694, 'Run2023C', 'm'),
        (370616, 371225, 'Run2023D', 'y'),
    ]
    
    for start, end, label, color in spans:
        ax.axvspan(run2time(start, run_info), run2time(end, run_info), color=color, alpha=0.1)
        mid_point = run2time((start + end) // 2, run_info)
        ax.text(mid_point, ymin + 15, label, rotation=90, verticalalignment='center', fontsize=22, weight='bold', color=color)
    
    #ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=(1, 15)))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    #ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%b'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))

    ax.grid()
    
    #ax.legend(loc='center right', fontsize = 28)
    #plt.tight_layout(rect=[0, 0, 1, 1])
    #plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
        
    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True)
    fig.savefig(output_path)
    plt.close(fig)

def plot_eff_by_time_run3(input_path_run3, run_info_path, region, output_path, fix_color=True, alpha=1.0):
    if type(region) is list:
        mid_label = 'RPC Efficiency'
    elif type(region) is str:
        mid_label = f'RPC {region} Efficiency'
    fig, ax = init_figure(
        figsize = (20, 9),
        fontsize = 24,
        com = 13.6,
        label1 = 'Work in Progress',
        label2 = f'2022, 2023 Data',
        mid_label = f'{mid_label}',
        loc = 0,
        ylabel = 'Efficiency [%]',
        xlim = None,
        ylim = None,
        xticks = None,
        yticks = None,
        log_scale = False,
    )
    run_info = pd.read_csv(run_info_path, index_col = False)

    ymin, ymax = 0, 100
    ax.set_xlim(datetime.strptime('2022/01/Jul', '%Y/%d/%b'), datetime.strptime('2023/01/Sep', '%Y/%d/%b'))
    ax.set_ylim(ymin, ymax)
    
    if type(region) is list:
        for i_region in region:
            ax, effs, runs = plot_eff_time(ax, input_path_run3, run_info, i_region, fix_color, alpha)     
        ax.legend(loc='center right', fontsize = 28) 
    elif type(region) is str:
        ax, effs, runs = plot_eff_time(ax, input_path_run3, run_info, region, fix_color, alpha)
    
    spans = [
        (355100, 355769, 'Run2022B', 'y'),
        (355862, 357482, 'Run2022C', 'm'),
        (357538, 357900, 'Run2022D', 'y'),
        (359356, 360327, 'Run2022E', 'm'),
        (360335, 362167, 'Run2022F', 'y'),
        (362362, 362760, 'Run2022G', 'm'),
        (366403, 367079, 'Run2023B', 'y'),
        (367770, 369694, 'Run2023C', 'm'),
        (370616, 371225, 'Run2023D', 'y'),
    ]
    
    for start, end, label, color in spans:
        ax.axvspan(run2time(start, run_info), run2time(end, run_info), color=color, alpha=0.1)
        mid_point = run2time((start + end) // 2, run_info)
        ax.text(mid_point, ymin + 15, label, rotation=90, verticalalignment='center', fontsize=16, weight='bold', color=color)
    
    #ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=(1, 15)))
    #ax.xaxis.set_major_locator(mdates.MonthLocator())
    #ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%b'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))

    ax.grid()
    
    #ax.legend(loc='center right', fontsize = 28)
    #plt.tight_layout(rect=[0, 0, 1, 1])
    #plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
        
    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True)
    fig.savefig(output_path)
    plt.close(fig)