"""Script to merge metric files.

Example
-------

> python scripts/merge_metrics.py

or

> python scripts/merge_metrics.py -s output/simulation/*/metrics/simulation_metrics_*.json

or

> python scripts/merge_metrics.py -o output/my_table.json

Authors
-------
- De Bruin, Jonathan
"""

# version 0.6.3

import argparse
import glob
import json
from pathlib import Path
import pandas as pd


def create_table_state_metrics(states):
    metrics = []

    for state in states:
        with open(state) as f:
            data = json.load(f)['data']['items']
            values = {}
            values['file_name'] = Path(state).name
            for item in data:
                if item['id'] == 'td':
                    continue
                # check if value is a list
                if item['value'] is not None and isinstance(item['value'], list):
                    for value in item['value']:
                        values[item['id'] + "_" + str(value[0])] = value[1]
                else:
                    values[item['id']] = item['value']
            metrics.append(values)

    return pd.DataFrame(metrics)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Merge metrics of multiple states into single table."
    )
    parser.add_argument(
        "-s",
        type=str,
        default="output/simulation/*/metrics/metrics_sim_*.json",
        help="states location")
    parser.add_argument(
        "-o",
        type=str,
        default="output/tables/data_metrics.csv",
        help="Output table location")
    args = parser.parse_args()

    # load states
    states = glob.glob(args.s)

    # merge results
    result = create_table_state_metrics(states)

    # store result in output folder
    Path(args.o).parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(Path(args.o))
    result.to_excel(Path(args.o).with_suffix('.xlsx'))
