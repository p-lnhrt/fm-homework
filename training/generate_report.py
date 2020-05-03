import argparse
import joblib
import os
import re
import sys

import pandas as pd
import sklearn.metrics as skmetrics

INPUT_FEATURES = ['residence_history', 'installment_rate', 'existing_credits', 'dependents', 'checking_balance',
                  'savings_balance', 'personal_status', 'installment_plan']
TARGET = 'default'


def preprocess_input_data(df):
    df[TARGET] = df[TARGET].map({1: 0, 2: 1})
    return df


def load_artifacts(train_file_path, test_file_path, model_file_path):
    train_data = pd.read_csv(train_file_path, header=0, usecols=[*INPUT_FEATURES, TARGET])
    train_data = preprocess_input_data(df=train_data)

    test_data = pd.read_csv(test_file_path, header=0, usecols=[*INPUT_FEATURES, TARGET])
    test_data = preprocess_input_data(df=test_data)

    trained_model = joblib.load(model_file_path)

    return train_data, test_data, trained_model


def compute_metrics(train_data, test_data, trained_model):
    metrics = dict()

    X_train, y_train = train_data[INPUT_FEATURES], train_data[TARGET]
    X_test, y_test = test_data[INPUT_FEATURES], test_data[TARGET]

    y_train_pred = trained_model.predict(X_train)
    y_test_pred = trained_model.predict(X_test)

    metrics.update({'train_precision': skmetrics.precision_score(y_train, y_train_pred)})
    metrics.update({'test_precision': skmetrics.precision_score(y_test, y_test_pred)})
    metrics.update({'train_recall': skmetrics.recall_score(y_train, y_train_pred)})
    metrics.update({'test_recall': skmetrics.recall_score(y_test, y_test_pred)})
    metrics.update({'train_f1': skmetrics.f1_score(y_train, y_train_pred)})
    metrics.update({'test_f1': skmetrics.f1_score(y_test, y_test_pred)})

    y_train_proba = trained_model.predict_proba(X_train)[:, 1]
    y_test_proba = trained_model.predict_proba(X_test)[:, 1]

    train_pre, train_rec, _ = skmetrics.precision_recall_curve(y_train, y_train_proba)
    test_pre, test_rec, _ = skmetrics.precision_recall_curve(y_test, y_test_proba)

    metrics.update({'train_pr_curve_auc': skmetrics.auc(train_rec, train_pre)})
    metrics.update({'test_pr_curve_auc': skmetrics.auc(test_rec, test_pre)})

    return metrics


def build_report(model_name, metrics):
    report_lines = [
        'TRAINING REPORT',
        'Model: {}'.format(model_name),
        '',
        'Training set metrics',
        '----------------------',
        'Precision: {:04.3f}'.format(metrics['train_precision']),
        'Recall: {:04.3f}'.format(metrics['train_recall']),
        'F1-score: {:04.3f}'.format(metrics['train_f1']),
        'PR curve AUC: {:04.3f}'.format(metrics['train_pr_curve_auc']),
        '',
        'Test set metrics',
        '----------------------',
        'Precision: {:04.3f}'.format(metrics['test_precision']),
        'Recall: {:04.3f}'.format(metrics['test_recall']),
        'F1-score: {:04.3f}'.format(metrics['test_f1']),
        'PR curve AUC: {:04.3f}'.format(metrics['test_pr_curve_auc'])
    ]

    return '\n'.join(report_lines)


def dump_report(report, output_dir_path, model_name):
    file_name = os.path.join(output_dir_path, 'training_report_{}.txt'.format(model_name))
    with open(file_name, 'w') as file:
        file.write(report)


def main(train_file_path, test_file_path, model_file_path, output_dir_path):
    train_data, test_data, trained_model = load_artifacts(train_file_path=train_file_path,
                                                          test_file_path=test_file_path,
                                                          model_file_path=model_file_path)

    model_name = re.search(pattern=r'(\w+)\.joblib', string=model_file_path).group(1)

    metrics = compute_metrics(train_data, test_data, trained_model)
    report = build_report(model_name=model_name, metrics=metrics)
    dump_report(report=report, output_dir_path=output_dir_path, model_name=model_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--train-file',
                        help='CSV training data file path on the local file system')

    parser.add_argument('--test-file',
                        help='CSV testing data file path on the local file system')

    parser.add_argument('--model',
                        help='Serialized model file on the local file system')

    parser.add_argument('--output-dir',
                        default='.',
                        help='Output directory path on the local file system')

    args = parser.parse_args(args=sys.argv[1:])

    main(train_file_path=args.train_file,
         test_file_path=args.test_file,
         model_file_path=args.model,
         output_dir_path=args.output_dir)
