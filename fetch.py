import time
from pathlib import Path
import shutil
import subprocess
import sys

from sklearn import datasets

command_result = subprocess.run(
    ["curl", "--silent", "ipinfo.io"], capture_output=True, text=True
)
print(command_result.stdout)

fetcher_names = [
    each
    for each in dir(datasets)
    if each.startswith("fetch_") and not ("openml" in each or "file" in each)
]

data_home = Path(datasets.get_data_home())

if data_home.exists():
    shutil.rmtree(data_home)

results = []
for name in fetcher_names:
    print(f"{name=}")
    tic = time.time()
    fetcher = getattr(datasets, name)
    try:
        fetcher()
        elapsed = time.time() - tic
        print(f"success in {elapsed:.2f}s")
        results.append({"name": name, "success": True, "elapsed": elapsed})
    except Exception as exc:
        elapsed = time.time() - tic
        print(f"error in {elapsed:.2f}s")
        results.append(
            {"name": name, "success": False, "elapsed": elapsed, "info": exc}
        )


succesful_results = [r for r in results if r["success"]]
erroring_results = [r for r in results if not r["success"]]

print()
print("-" * 80)
print("Success")
for r in succesful_results:
    print()
    print(f"{r['name']}: {r['elapsed']:.2f}s")
print("-" * 80)

print()
print("-" * 80)
print("Errors")
for r in erroring_results:
    print(f"{r['name']} {r['elapsed']:.2f}s {r['info']}")
print("-" * 80)

if erroring_results:
    print()
    print("Some fetchers failed, see above")
    sys.exit(1)
