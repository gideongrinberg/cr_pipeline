import tqdm
import pandas as pd
import lightkurve as lk
import matplotlib.pyplot as plt

from glob import glob
from astroquery.mast import Tesscut

from pipeline.complexity import is_complex
from pipeline.plotting import make_plot
from pipeline.lightcurves import make_lightcurves, load_lc

import warnings
warnings.filterwarnings("ignore")

# Download lightcurves
tics = []
for csv in glob("tests/data/*/*.csv"):
    df = pd.read_csv(csv)
    tics.extend(list(df["TICID"]))

crs = []
for csv in glob("tests/data/complex/*.csv"):
    df = pd.read_csv(csv)
    crs.extend(list(df["TICID"]))

controls = []
for csv in glob("tests/data/control/*.csv"):
    df = pd.read_csv(csv)
    controls.extend(list(df["TICID"]))


# # Uncomment to download only missing targets
# sectors = []
# for tic in tqdm.tqdm(tics):
#     for sector in list(Tesscut.get_sectors(objectname=f"TIC {tic}")["sector"]):
#         sectors.append((tic, sector))

# exists = []
# missing = []

# for tic, sector in tqdm.tqdm(sectors):
#     if os.path.isfile(f"./lightcurves/{tic}_{sector}.csv"):
#         exists.append((tic, sector))
#     else:
#         missing.append((tic, sector))

# missing = pd.DataFrame(data=missing, columns=["TICID", "Sector"])
# for tic in tqdm.tqdm(missing["TICID"].unique()):
#     sectors = list(missing[missing["TICID"] == tic]["Sector"].unique())
#     make_lightcurves(f"TIC {tic}", sectors=sectors)
# # End download missing

# # Uncomment to run the first time download
# start = time.time()
# for tic in tqdm.tqdm(tics):
#     make_lightcurves(f"TIC {tic}")
# end = time.time()
# print(f"Finished in {end - start} seconds.")
# # End first time download


# Run the complexity checker and save the output to ./output/results.csv
results = []
for file in tqdm.tqdm(glob("lightcurves/*.csv")):
    tic, sector = file.split("/")[1].strip(".csv").split("_")
    tic = f"TIC {tic}"

    try:
        results.append((tic, sector, is_complex(load_lc(tic, sector))))
    except:
        results.append((tic, sector, None))

results = pd.DataFrame(results, columns=["TIC", "Sector", "Complex"]).replace(-1, None)
results.to_csv("./tests/output/results.csv")


# Compare results with labels
# labels = pd.read_csv("./tests/output/labels.csv") # Generate with ../guis/lccheck.py run on the list of test stars.

# results = results.rename(columns={"Complex": "pipeline"})
# results["lc"] = results["TIC"].astype(str) + "_" + results["Sector"].astype(str)
# results = results[["lc", "pipeline"]]

# labels = labels.rename(columns={"Complex": "label"})
# labels["lc"] = labels["TIC"].astype(str) + "_" + labels["Sector"].astype(str)
# labels = labels[["lc", "label"]]

# merged = pd.merge(labels, results, on="lc", how="left")

# total = merged.shape[0]
results["lc"] = results["TIC"] + "_" + results["Sector"]
results["pipeline"] = results["Complex"]
results["label"] = results["TIC"].isin([f"TIC {tic}" for tic in crs])

merged = results.dropna()
total = len(merged)
errors = merged["pipeline"].isna().sum()
false_positives = merged[(merged["pipeline"] == True) & (merged["label"] == False)].shape[0]
false_negatives = merged[(merged["pipeline"] == False) & (merged["label"] == True)].shape[0]

errors_pct = errors / total * 100
fp_pct = false_positives / merged[merged["label"] == True].shape[0] * 100
fn_pct = false_negatives / merged[merged["label"] == False].shape[0] * 100

true_positives = merged[(merged["pipeline"] == True) & (merged["label"] == True)].shape[0]
true_negatives = merged[(merged["pipeline"] == False) & (merged["label"] == False)].shape[0]
accuracy = (true_positives + true_negatives) / total * 100

print(f"Total samples: {total}")
print(f"Errors (pipeline outputted None): {errors} ({errors_pct:.2f}%)")
print(f"False Positives (pipeline True, label False): {false_positives} ({fp_pct:.2f}%)")
print(f"False Negatives (pipeline False, label True): {false_negatives} ({fn_pct:.2f}%)")
print(f"Accuracy: {accuracy:.2f}%")

merged.to_csv("./tests/output/summary.csv")

fn_lcs = list(merged[(merged["label"] == True) & (merged["pipeline"] == False)]["lc"])
for lc in tqdm.tqdm(fn_lcs):
    tic, sector = lc.strip("TIC ").split("_")

    lc = load_lc(f"TIC {tic}", sector)
    try:
        make_plot(lc)
    except: 
        tqdm.tqdm.write(f"Failed to produce plot for TIC {tic}:{sector}")

    plt.savefig(f"./tests/figs/fn/{tic}_{sector}.png")
    plt.close("all")


fp_lcs = list(merged[(merged["label"] == False) & (merged["pipeline"] == True)]["lc"])
for lc in tqdm.tqdm(fp_lcs):
    tic, sector = lc.strip("TIC ").split("_")

    lc = load_lc(f"TIC {tic}", sector)
    try:
        make_plot(lc)
    except: 
        tqdm.tqdm.write(f"Failed to produce plot for TIC {tic}:{sector}")

    plt.savefig(f"./tests/figs/fp/{tic}_{sector}.png")
    plt.close("all")

tp_lcs = list(merged[(merged["label"] == True) & (merged["pipeline"] == True)]["lc"])
for lc in tqdm.tqdm(tp_lcs):
    tic, sector = lc.strip("TIC ").split("_")

    lc = load_lc(f"TIC {tic}", sector)
    try:
        make_plot(lc)
    except: 
        tqdm.tqdm.write(f"Failed to produce plot for TIC {tic}:{sector}")

    plt.savefig(f"./tests/figs/tp/{tic}_{sector}.png")
    plt.close("all")