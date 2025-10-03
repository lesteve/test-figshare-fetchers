from sklearn import datasets

fetcher_names = [
    each for each in dir(datasets) if each.startswith("fetch_") and not "openml" in each
]

for name in fetcher_names:
    print(f"{name=}")
    fetcher = getattr(datasets, name)
