import numpy as np
import lightkurve as lk
import astropy.units as u
import matplotlib.pyplot as plt

from wotan import flatten
from scipy.signal import find_peaks

# from pipeline.plotting import plot_lc
from pipeline.lightcurves import load_lc, load_lc_pandas

# def is_complex(lc, plot=False, wrap=True):
#     # nlc = lc.normalize()
#     nlc = lc
#     pg = nlc.to_periodogram()
#     period = pg.period_at_max_power

#     if period >= u.Quantity(2, u.day): # question: right units? should it be sidereal/julian?
#         return False
    
#     flc = nlc.remove_outliers().fold(period=period)

#     # OLD BINNING CODE: Bin using one of the below, then make phase and flux = blc["phase"/"flux"].value
#     # blc = flc.bin(time_bin_size=u.Quantity(150, u.second))
#     # blc = flc.bin(binsize=len(flc.time) // 300)
#     # blc = flc.bin(time_bin_size=u.Quantity(300, u.s))
#     # blc = flc.bin(binsize=np.ptp(flc["flux"].value)//300)

#     # Wrap phase to start at 0
#     cycle_length = np.max(flc["time"].value) - np.min(flc["time"].value)
   
#     full_phase = (flc["time"].value - np.min(flc["time"].value)) % cycle_length
#     full_flux = flc["flux"].value # unbinned flux and phase

#     # Bin to 300 points per cycle
#     # Lightkurve can't do this for some reason. See https://github.com/lightkurve/lightkurve/issues/1271
#     nbins = 300
#     bin_edges = np.linspace(0, cycle_length, nbins + 1)
#     bin_indices = np.digitize(full_phase, bin_edges, right=False)

#     phase = np.empty(nbins) # binned phase
#     flux = np.empty(nbins) # binned flux

#     for i in range(1, nbins + 1): # take the average value for each bin
#         mask = (bin_indices == i)
#         if np.any(mask):
#             phase[i-1] = np.mean(full_phase[mask])
#             flux[i-1]  = np.mean(full_flux[mask])
#         else: 
#             phase[i-1] = (bin_edges[i-1] + bin_edges[i]) / 2
#             flux[i-1]  = np.nan # empty bin = nan
    
#     # phase = np.concatenate((phase - cycle_length, phase, phase + cycle_length))
#     # flux = np.concatenate(flux, flux, flux)
#     # Create spline
#     _, trend_lc, _ = flatten(
#         phase,
#         flux,
#         method="pspline",
#         max_splines=10,
#         stdev_cut=2,
#         return_trend=True,
#         return_nsplines=True,
#     )

#     # Find sharp local minima
#     residuals = (flux - trend_lc) / 1

#     dres = np.diff(residuals)  # noise level
#     noise = np.percentile(np.abs(dres - np.median(dres)), 68)

#     # TODO fix these based on paper
#     min_width = 0.2*np.max(phase)
#     min_height = 2 * noise

#     peaks, _ = find_peaks(-residuals, width=min_width, height=min_height) # TODO figure this shit out

#     residuals = -residuals

#     if plot:
#         fig, axes = plt.subplots(2, 1, figsize=(6,6))
#         axes[0].scatter(full_phase, full_flux, s=8, color="gainsboro")
#         axes[0].scatter(phase, flux, s=8, color="black")
#         axes[0].plot(phase, trend_lc, color="limegreen")
#         axes[0].scatter(phase[peaks], flux[peaks], color="red", marker="x", s=50, label="Peaks")    

#         axes[1].plot(pg.frequency, pg.power, linewidth=0.5, color="black")
        

#         return (len(peaks) >= 3, fig)

#     return len(peaks) >= 3

def _count_harmonics(lc, tolerance=0.15):
    pg = lc.to_periodogram()
    period =  pg.period_at_max_power

    if period.value >= 2:
        return []

    expected_harmonics = []
    for i in range(1,9):
        expected_harmonics.append(period.value/i)

    peaks, properties = find_peaks(pg.power, distance=120, height=pg.max_power.value*tolerance)
    peak_periods = [pg.period[idx].value for idx in peaks]

    found_harmonics = []
    for i, period in enumerate(peak_periods):
        in_range = 0.9 * expected_harmonics[i] <= period <= 1.1 * expected_harmonics[i]
        if in_range:
            found_harmonics.append((period, properties["peak_heights"][i]))

    return found_harmonics

def is_complex(lc):
    return len(_count_harmonics(lc)) >= 3
    
