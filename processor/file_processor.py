import pandas as pd

def process_file(file_path):

    total = 0

    # Generator style reading (chunk wise)
    for chunk in pd.read_csv(file_path, chunksize=10):
        total += chunk["value"].sum()

    return total