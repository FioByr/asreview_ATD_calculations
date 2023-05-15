import os
import pandas as pd
import json
import asreview
import numpy as np
import argparse
import glob
from pathlib import Path


os.chdir("C:/Users/fionn/Documents/ASReview/sim_ARFI_makita")

#df = pd.read_csv("data_tds.csv")

def average_record_TD(df, prior=False):
    df['average_record_TD'] = df.iloc[:,2:].mean(axis=1)
    return df

def average_simulation_TD(data, priors=False):
    df.loc['average_simulation_TD'] = df.iloc[:, 2:-1].mean(axis=0)
    return df

average_record_TD(df)

average_simulation_TD(df)

# display entire df
pd.set_option('display.max_rows', None)

sim_ATD = df.iloc[-1].mean()
print(f"sim_ATD: {sim_ATD:.50f}")

record_ATD = df['average_record_TD'].mean()
print(f"record_ATD: {record_ATD:.50f}")

def get_td_values(df, version=None):

    average_record_TD(df)

    average_simulation_TD(df)

    avg_record_TD = df['average_record_TD'].dropna().to_list()

    record_ATD = df['average_record_TD'].mean()

    avg_sim_TD = df.loc['average_simulation_TD'].dropna().to_list()

    sim_ATD = df.iloc[-1].mean()

    result = {
        "asreviewVersion": asreview.__version__,
        "apiVersion": version,
        "data": {
            "items": [{
                "id": "ratd",
                "title": "Record-average time to discovery",
                "value": record_ATD
            }, {
                "id": "artd",
                "title": "Average-record-time to discovery",
                "value": avg_record_TD
            }, {
                "id": "satd",
                "title": "Simulation-average time to discovery",
                "value": sim_ATD
            }, {
                "id": "astd",
                "title": "Average-simulation-time to discovery",
                "value": avg_sim_TD
            }]
        }
    }

    return result

#td_values = get_td_values(df)
                                
#print_metrics(td_values)

def split_file_paths(file_paths):
    simulations = {}
    for path in file_paths:
        dirname = os.path.dirname(path)
        if dirname not in simulations:
            simulations[dirname] = []
        simulations[dirname].append(path)
    return simulations

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Merge tds of multiple metrics into single table."
    )
    parser.add_argument(
        "-s",
        type=str,
        default="output/simulation/*/tables/data_tds.csv", 
        help="td tables location")
    parser.add_argument(
        "-o",
        type=str,
        default="../metrics/td_values.json",
        help="Output table location")
    args = parser.parse_args()

    # load tables
    tables = glob.glob(args.s)
    simulations = split_file_paths(tables)
    simulations.items()

    # merge results for each simulation
    for dirname, sim_metrics in simulations.items():
        for metric_file in sim_metrics:
            df = pd.read_csv(metric_file)
            td_values = get_td_values(df)
            td_json = json.dumps(td_values, indent=4)

        # store result in output folder
            output_path = os.path.abspath(os.path.join(dirname, args.o))
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
            with open(output_path, "w") as f:
                f.write(td_json)
        

           







