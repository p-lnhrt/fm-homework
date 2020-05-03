python split_data.py --data ./input/credit.csv --output-dir ./data --test-ratio 0.3 

python train_model.py --data ./data/train.csv --output-dir ./models

python generate_report.py --train-file=./data/train.csv --test-file=./data/test.csv --model=./models/CDEFAULT_RF_20200503120903.joblib --output-dir=./reports

                            
