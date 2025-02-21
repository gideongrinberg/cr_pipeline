# Complex Rotator Detection Pipeline

## Structure

### `pipeline.lightcurves`
- `make_lightcurves(tic, sector=None)` downloads and detrends cutouts of the given sector, and converts them into lightcurves. If a list of sectors is not provided, all available sectors will be downloaded.

- `load_lc(tic, sector)` loads the given lightcurve from the `lightcurves/` directory. Returns `None` if the provided lightcurve does not exist.

## `pipeline.plotting`
- `plot_lc(lc)` creates a phase-folded plot of a lightcurve

- `make_plot(lc)` creates a plot with a phase-folded lightcurve and its periodogram. It labels the harmonics on the periodogram. Helpful for testing.

## `pipeline.complexity`
- `is_complex(lc)` returns `True` if the lightcurve is correct and `False` otherwise.

- `_count_harmonics(lc)` detects harmonics in a lightcurve's periodogram. Used internally by `is_complex` and `make_plot`. Returns a list of tuples containing each harmonics' period and power. 

## Testing

The scripts in `tests/` run the pipeline against a 41 known complex rotators and 15 non-complex objects (10 stars with transiting exoplanets and 5 eclipsing binaries), for a total of 295 distinct sectors. 

The pipeline accurately identifies around 88% of complex rotators. Some of the objects it fails to identify are of ambigious complexity, such as TIC 65347864. 

## GUIs

The scripts in `guis/` are `NiceGUI`-based apps that allow users to view and label lightcurves. 

