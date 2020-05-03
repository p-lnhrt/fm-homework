import argparse
import datetime as dt
import joblib
import os
import sys

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

EXPERIMENT_ID = 'CDEFAULT_RF'
SEED = 42
NUMERICAL_FEATURES = ['residence_history', 'installment_rate', 'existing_credits', 'dependents']
CATEGORICAL_FEATURES = ['checking_balance', 'savings_balance', 'personal_status', 'installment_plan']
TARGET = 'default'


def preprocess_input_data(df):
    df[TARGET] = df[TARGET].map({1: 0, 2: 1})
    return df


def build_model():
    classifier = RandomForestClassifier(n_estimators=100,
                                        criterion='gini',
                                        class_weight='balanced',
                                        random_state=SEED,
                                        max_depth=3,
                                        min_samples_leaf=7)

    preprocessor = ColumnTransformer(
        transformers=[
            ('encoder', OneHotEncoder(), CATEGORICAL_FEATURES)
        ])

    return Pipeline(steps=[('preprocessor', preprocessor),
                           ('classifier', classifier)])


def dump_model(model, output_dir_path):
    current_timestamp = dt.datetime.strftime(dt.datetime.now(), '%Y%m%d%H%M%S')
    file_name = '{}.joblib'.format('_'.join([EXPERIMENT_ID, current_timestamp]))
    joblib.dump(model, os.path.join(output_dir_path, file_name))


def main(input_file_path, output_dir_path):
    input_data = pd.read_csv(input_file_path, header=0, usecols=[*NUMERICAL_FEATURES, *CATEGORICAL_FEATURES, TARGET])
    input_data = preprocess_input_data(df=input_data)

    input_features = NUMERICAL_FEATURES + CATEGORICAL_FEATURES

    model = build_model()
    model.fit(input_data[input_features], input_data[TARGET])
    dump_model(model=model, output_dir_path=output_dir_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--data',
                        help='CSV input data file path on the local file system')

    parser.add_argument('--output-dir',
                        default='.',
                        help='Output directory path on the local file system')

    args = parser.parse_args(args=sys.argv[1:])

    main(input_file_path=args.data, output_dir_path=args.output_dir)
