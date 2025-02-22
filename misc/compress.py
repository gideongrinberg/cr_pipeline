import numpy as np
import pandas as pd

targets = pd.read_csv("./misc/targets_full.csv")
chunks = np.array_split(targets, 2)

for i, chunk in enumerate(chunks):
    chunk.to_parquet(f"./misc/targets/targets_{i + 1}.parquet", compression="snappy")