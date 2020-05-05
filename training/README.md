##### Author: Pierre LIENHART
##### Contact: pierre.lienhart[at]gmail.com

# FairMoney Machine Learning Engineer Homework - Training exercise 
This exercice is divided into three parts each with a corresponding Python script. 

## 1. Input data set split
Splitting an input data set into a train and test set in carried out using the `split_data.py` Python script which can be
launched using the following command:

```bash
python split_data.py --data ./input/credit.csv --output-dir ./data --test-ratio 0.3 
```

### 1.1. Implementation notes
We choose a stratified split to ensure that the minority class proportion remains the same after the split. 

## 2. Model training
Model training can be carried out using the `train_model.py` Python script which can be launched using the following 
command:

```bash
python train_model.py --data ./data/train.csv --output-dir ./models
```

### 2.1. Implementation notes
#### 2.1.1. Modelling
The input dataset consists in 4 categorical variables and 4 numerical variables and 1 target variable.

Two categorical variables (`checking_balance` and `savings_balance`) include missing values (labelled `unknown`). These 
missing values were not imputed nor discarded and were encoded like all the other categories. This choice has been made: 
1. for simplicity,
2. because in our specific use case, a missing value can be information on its own.

A next modelling step would consider trying to impute the above-mentionned missing values and/or try to consider the 
`checking_balance` and `savings_balance` variables not as simple categorical variables but as ordinal variables.

Aside from one-hot encoding categorical variables, our preprocessing simply consists in recoding the target variable 
to better match `sklearn`'s encoding for a target binary variable (`0`/`1` or `-1`/`1`). In particular, numerical 
variables were not scaled as it was not required by our use of decision trees, nor transformed (ex: log-transformed) as 
the examination of their distribution show this was not necessary.  

We choose a random forest as classifier. Hyperparameter tuning has been performed using a grid search (using the 
F1-score as metric) and a 5-fold stratified cross-validation. As an imbalanced problem (70%/30% class balance) and to 
avoid to create a majority-class bias, samples were weighted using their class inverse frequency (cf. 
`class_weight='balanced'` argument).

**Notice on performance**:
Assessed model performance seems rather mediocre at first sight (cf. generated metrics report): 0.43 test precision 
and 0.76 test recall. From a business perspective:
* The model avoids to grant a loan to 76% of the bad debtors.
* Among all the declined loan submissions however, 57% were actually sound projects.

However, we do not know how business values a missed credit opportunity and a default. Therefore, next modelling steps 
would include:
* Experimenting with other model specifications
* Experimenting with model selection metrics that give different weights to true and false positives.

#### 2.1.2. Hyperparameter tuning
Model training has been understood as not including the hyperparameter tuning (and as not required, the code related to 
the hyperparameter tuning of our model has not been included). In a perspective of frequent and automatic re-trainings, 
hyperparameter tuning is indeed not included in trainings for two main reasons:
* Hyperparameter tuning can be costly
* Hyperparameter tuning is part of the model specification which should not change with each training. Furthermore,
 as model specification may require the intervention of the data scientist, we may not want to automate it. 

#### 2.1.3. Model serialization
Trained model are serialized in the joblib format and exported to the local file system.

### 2.2. Possible improvements (excluding modelling)
We can make suggestions of improvement for this script:
* The model specification is currently hard-coded into the script. We could leverage the fact that this specification 
is included in the model file. Re-training a model could therefore be done by simply using the latest model.
* The input feature order is currently hard-coded into the script and it would be better if it were attached to the 
model as metadata.
* We could provide support other model serialization formats (pickle, HDF5, etc.) and model repositories. This would 
imply to increase the code's modularity.

## 3. Training report generation 
A short model training report can be generated using the `generate_report.py` Python script which can be launched using 
the following command:

```bash
python generate_report.py --train-file=./data/train.csv --test-file=./data/test.csv --model=./models/CDEFAULT_RF_20200503120903.joblib --output-dir=./reports
```

### 3.1. Implementation notes
This script generated report as a simple text (.txt) file.

As our classification problem is imbalanced:
* We chose not to include the accuracy in our metrics
* We chose not to use the ROC curve and the associated area-under-curve (AUC) but preferred the Precision/Recall (PR) 
curve and its AUC.

### 3.2. Possible improvements
Possible improvements to training report generation would include:   
* Including curves or more generally plots which would in turn require the report to be generated in another appropriate 
format (PDF, HTML, etc.).
* We currently provide single-point estimation on performance metrics. Computing their respective standard deviations would
be a must-have but requires a cross-validation procedure.  
* The current choice of metrics depends on our problem.
* Refactoring of the report generation and export into a dedicated object. 
curl -i -H "Content-Type: application/json" -X POST --data '{"checking_balance":"unknown","savings_balance":"unknown","installment_rate":4,"personal_status":"single male","residence_history":1,"installment_plan":"none","existing_credits":1,"dependents":1}' http://localhost:5000/inference/AA1

## 4. Common possible improvements 
All scripts would in our view greatly benefit from the following improvement:
* Addition of CLI argument validation,
* Addition of data validation,
* Loosening the coupling between our script and the model input data,
* Addition of doctrings and/or type hints,
* Addition of unit and integration tests,
* Addition of a *CHANGELOG.md* file (depends on the versioning policy),
* Addition of a complexity analysis where relevant.

Overall much of what has been developed in this application (web service included) is made available to any ML project by 
(fairly new) tools such as [MLflow](https://mlflow.org/docs/latest/index.html).


