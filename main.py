import os
import json
import argparse
from multiprocessing import Pool
from processor.file_processor import process_file
from utils.timer import time_it


def get_files(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder)]


@time_it
def baseline(files):

    results = []
    for file in files:
        results.append(process_file(file))

    return results


@time_it
def optimized(files):

    with Pool() as pool:
        results = pool.map(process_file, files)

    return results


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["baseline", "optimized"], required=True)

    args = parser.parse_args()

    files = get_files("bulk_data")

    if args.mode == "baseline":
        _, baseline_time = baseline(files)

    else:
        _, optimized_time = optimized(files)

        # Run baseline again for comparison
        _, baseline_time = baseline(files)

        speedup = baseline_time / optimized_time

        result = {
            "filesProcessed": len(files),
            "baselineSeconds": round(baseline_time, 2),
            "optimizedSeconds": round(optimized_time, 2),
            "speedupX": round(speedup, 2),
            "methodUsed": "multiprocessing"
        }

        os.makedirs("output", exist_ok=True)

        with open("output/performance_results.json", "w") as f:
            json.dump(result, f, indent=4)


if __name__ == "__main__":
    main()