import random
import pandas as pd
from astroquery.mast import Catalogs

df = pd.read_csv("./tests/data/exoplanets.csv", comment="#")
df = df[df["disc_facility"] == "Transiting Exoplanet Survey Satellite (TESS)"]

tics = []
for i in range(5):
    while True:
        try:
            name = random.choice(df["hostname"].unique())
            results = Catalogs.query_object(name, catalog = "TIC")
            break
        except:
            pass

    tics.append(results[0]["ID"])


with open("./tests/data/control/transits.csv", "w") as f:
    f.write("TICID\n")
    for tic in tics:
        f.write(tic + "\n")
    


