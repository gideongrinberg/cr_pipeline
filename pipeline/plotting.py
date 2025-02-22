"""This module contains various functions for visualizing lightcurves."""

import numpy as np
import matplotlib.pyplot as plt

import astropy.units as u

from pipeline.lightcurves import load_lc
from pipeline.complexity import _count_harmonics


def make_plot(lc):
    pg = lc.to_periodogram()
    harmonics = _count_harmonics(lc)

    flc = lc.fold(period=pg.period_at_max_power)
    blc = flc.bin(time_bin_size=u.Quantity(300, u.s))

    fig, axes = plt.subplots(2, 1, figsize=(6, 6))

    axes[0].scatter(flc["time"].value, flc["flux"].value, s=8, color="gainsboro")
    axes[0].scatter(blc["time"].value, blc["flux"].value, s=8, color="black")

    axes[1].plot(pg.frequency, pg.power, linewidth=0.5, color="black")
    for harmonic in harmonics:
        x, y = harmonic
        axes[1].scatter(1 / x, y, marker="x", color="red")

    axes[1].set_xlim(-1, 50)
    fig.suptitle(
        f"{lc.meta['TIC']}, Sector {lc.meta['SECTOR']}\nPeriod: {str(pg.period_at_max_power)}"
    )

    return fig


def plot_lc(lc):
    nlc = lc.normalize()
    flc = nlc.remove_outliers().fold(period=nlc.to_periodogram().period_at_max_power)

    blc = flc.bin(binsize=len(flc.time) // 300)

    phase = blc["time"].value
    flux = blc["flux"].value

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.scatter(x=flc["time"].value, y=flc["flux"].value, alpha=0.005, color="gainsboro")
    ax.scatter(x=phase, y=flux, s=6, color="black")

    ax.set_xlabel("Phase")
    ax.set_ylabel("Flux")

    return fig