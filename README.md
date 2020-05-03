python split_data.py --data ./input/credit.csv --output-dir ./output --test-ratio 0.3 

python train_model.py --data ./output/train.csv --output-dir ./output

python generate_report.py --train-file=./output/train.csv --test-file=./output/test.csv --model=./output/CDEFAULT_RF_20200503120903.joblib --output-dir=./output

