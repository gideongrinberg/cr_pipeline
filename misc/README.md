This folder contains the list of M dwarf targets, generating from the TIC version 8.2 using the query in `mast_query.sql`. `targets.csv` contains a list of targets by TIC, RA and Dec.

The list of targets with all of the columns from the TIC is stored in `targets/`. To meet Github's storage limits, the list has been split into two parquet files. These can be loaded using Pandas, but they can also be loaded and queried using duckdb or similar software, which is much faster. 

Also, the php script is for saving the lightcurves from coiled.