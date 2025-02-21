import glob
import shutil
import pandas as pd
import lightkurve as lk

from pipeline import unpopular
from astroquery.mast import Catalogs
from astrocut import cube_cut_from_footprint

def _get_sector(filename):
    if "/" in filename:
        filename = filename.split("/")[-1]

    return int(filename.split("-")[1].strip("s"))


def _download_cutouts(tic=None, ra=None, dec=None, cutout_size=50, sectors=None):
    if tic is None and (ra is None and dec is None):
        raise ValueError("_download_cutouts requires ra/dec or TIC")
    
    if tic is not None:
        results = Catalogs.query_object(objectname=tic, catalog="TIC")
        ra = results[0]["ra"]
        dec = results[0]["dec"]

    return cube_cut_from_footprint(
        coordinates=f"{ra} {dec}",
        cutout_size=cutout_size,
        sequence=sectors,
        output_dir=f"./cutouts/",
    )


def make_lightcurves(tic, ra=None, dec=None, sectors=None):
    results = []

    if ra is not None and dec is not None:
        cutouts = _download_cutouts(ra=ra, dec=dec, sectors=sectors)
    else:
        cutouts = _download_cutouts(tic)

    for cutout in cutouts:
        s = unpopular.Source(cutout, remove_bad=True)

        s.set_aperture(rowlims=[25, 25], collims=[25, 25])
        s.add_cpm_model(exclusion_size=5, n=64, predictor_method="similar_brightness")

        s.set_regs([0.1])
        s.holdout_fit_predict(k=100)

        apt_detrended_flux = s.get_aperture_lc(data_type="cpm_subtracted_flux")

        sector = _get_sector(cutout)
        path = f"./lightcurves/{tic.split(' ')[1]}_{sector}.csv"

        pd.DataFrame({
            "time": list(s.time),
            "flux": list(apt_detrended_flux)
        }).to_csv(path, index=False)

        results.append(path)

    for f in glob.glob("cutouts/**"):
        shutil.rmtree(f)
    
    return results
  
def load_lc(tic, sector):
    """
    Loads a lightcurve as a lightkurve.LightCurve
    """
    try:
        df = pd.read_csv(f"./lightcurves/{tic.split(' ')[1]}_{sector}.csv")
    except:
        print("Could not open lightcurve")
        return

    lc = lk.LightCurve(time=df["time"], flux=df["flux"])
    lc.meta["TIC"] = tic
    lc.meta["SECTOR"] = sector

    return lc

def load_lc_pandas(tic, sector):
    """
    Loads a lightcurve as a Pandas dataframe with columns time and flux
    """
    try:
        df = pd.read_csv(f"./lightcurves/{tic.split(' ')[1]}_{sector}.csv")
        return df
    except:
        print("Could not open lightcurve")
        raise Exception()
    
    


