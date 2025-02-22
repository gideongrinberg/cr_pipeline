"""This module contains various functions for checking the complexity of a given lightcurve"""

import lightkurve as lk
from scipy.signal import find_peaks

def _count_harmonics(
    lc: lk.LightCurve, height: float = 0.15
) -> list[tuple[float, float]]:
    """Find the harmonics in the L-S periodogram of a given lightcurve.
    WARNING: Does not actually count the harmonics!

    Args:
        lc (lk.LightCurve)
        height (float, optional): The minimum height of a peak as a fraction of the main harmonic. Defaults to 0.15.

    Returns:
        list[tuple[float, float]]: A list containing each harmonic as a tuple of period and power.
    """

    pg = lc.to_periodogram()
    period = pg.period_at_max_power

    if period.value >= 2:
        return []

    expected_harmonics = []
    for i in range(1, 9):
        expected_harmonics.append(period.value / i)

    peaks, properties = find_peaks(
        pg.power, distance=120, height=pg.max_power.value * height
    )
    peak_periods = [pg.period[idx].value for idx in peaks]

    found_harmonics = []
    for i, period in enumerate(peak_periods):
        in_range = 0.9 * expected_harmonics[i] <= period <= 1.1 * expected_harmonics[i]
        if in_range:
            found_harmonics.append((period, properties["peak_heights"][i]))

    return found_harmonics

def is_complex(lc: lk.LightCurve) -> bool:
    """Check if a given lightcurve is complex by counting the number of harmonics."""
    return len(_count_harmonics(lc)) >= 3
