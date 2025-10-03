import time
from pathlib import Path
import shutil

from sklearn import datasets

fetcher_names = [
    each for each in dir(datasets) if each.startswith("fetch_") and not ("openml" in each or "file" in each)
]

data_home = Path(datasets.get_data_home())

if data_home.exists():
    shutil.rmtree(data_home)

for name in fetcher_names:
    print(f"{name=}")
    tic = time.time()
    fetcher = getattr(datasets, name)
    fetcher()
    elapsed = time.time() - tic
    print(f"{elapsed=}")

