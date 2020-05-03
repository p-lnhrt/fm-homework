import argparse
import os
import sys

import pandas as pd
from sklearn.model_selection import train_test_split

SEED = 42
TARGET = 'default'
INPUT_FEATURES = ['checking_balance', 'savings_balance', 'installment_rate', 'personal_status', 'residence_history',
                  'installment_plan', 'existing_credits', 'dependents']


def main(input_file_path, output_dir_path, test_ratio):
    input_data = pd.read_csv(input_file_path, header=0, usecols=[*INPUT_FEATURES, TARGET])

    datasets = train_test_split(input_data,
                                test_size=test_ratio,
                                random_state=SEED,
                                shuffle=True,
                                stratify=input_data[TARGET])

    output_paths = [os.path.join(output_dir_path, filename) for filename in ('train.csv', 'test.csv')]

    for dataset, output_path in zip(datasets, output_paths):
        dataset.to_csv(output_path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--data',
                        help='CSV input data file path on the local file system')

    parser.add_argument('--output-dir',
                        default='.',
                        help='Output directory path on the local file system')

    parser.add_argument('--test-ratio',
                        default=0.3,
                        type=float,
                        help='Share of the input data to be dumped into the test dataset')

    args = parser.parse_args(args=sys.argv[1:])

    assert (args.test_ratio > 0) and (args.test_ratio < 1), 'Test ratio must take values between 0 and 1'

    main(input_file_path=args.data, output_dir_path=args.output_dir, test_ratio=args.test_ratio)
