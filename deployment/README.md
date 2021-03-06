##### Author: Pierre LIENHART
##### Contact: pierre.lienhart[at]gmail.com

# FairMoney Machine Learning Engineer Homework - Deployment exercise 

## 1. Design overview
The purpose of this exercise is to develop a web application that exposes trained model to a client that can:
* List all available models
* Send a single observation to the web server which responds with the prediction from the chosen model
* Send a batch of observations to the web server which responds with the predictions from the chosen model

We chose to develop this web server using [Flask](https://flask.palletsprojects.com/en/1.1.x/). The `predictionws` Python
package gathers the application's code which consists in the following modules:
* `__init__.py`: Contains the app's factory function `create_app`. Used as the application's entry point when run using 
`flask run` (see Launching the application below).
* `bases.py`: Gathers the different abstract base classes which explicit the interfaces used by the application. 
* `config.py`: Contains the application's configuration.
* `predictor.py`: Gathers all the code related to producing a prediction. 
* `db.py`: Gathers all the code related to the model metadata database used by the web service.
* `views.py`: Gathers the application's view functions.
* `warehouse.py`: Gathers all the code related to the model warehouse used by the web service.

From a design perspective, the application's database contains the metadata for all the available trained models. This database
is distinct from the model warehouse where the serialized model files are physically stored and from where they are imported.

When a client sends data to the server (choosing a model at the same time), the application would query the  database 
for that model metadata, retrieve the model from the appropriate model warehouse and inject the deserialized model file 
and metadata to the object that encapsulates the prediction logic.

This homework implements this concept locally:
* The model metadata database is simulated using a JSON file (one metadata dictionary per model) placed in 
`deployment/database/models_metadata.json`. We provide the application with this path using the `MODEL_METADATA_DB` configuration.
* The model warehouse is simulated using a local directory (`deployment/model_warehouse`). We provide the application 
with this path using the `MODEL_WAREHOUSE` configuration.

## 2. Launching the application
The application is deployed as a Docker container which embeds all the required Python dependencies specified in the 
exercise's *requirement.txt* file.  

Change your current working directory to the `deployment` directory:

```bash
cd deployment
```

Build the exercise's Docker image:

```bash
docker build -t fmhomework:latest .
```

Launch the container using the Docker image you just built with the following command:

```bash
docker run --init -d -p 5000:5000 fmhomework:latest
```

The web server now runs from within the Docker container, is bound to its port 5000 and is opened to no-local 
connections (host set to 0.0.0.0). The container's 5000 port has been published to the host's (your local machine) port 
5000.

## 3. Using the application
We will be using the cURL command to send request to our running web server. First, open a new terminal.

### 3.1. Querying for available models
To query the server for the available trained models, use the following command:

```bash
curl -X GET http://localhost:5000/models
```

The command should return a JSON-formatted response that consists in a dictionary with a single `'model'`  field. The 
latter consists in a list of dictionaries, each containing the model ID and the URIs the client can use to send 
data to it. For example the example command above should return:

```bash
{
  "models": [
    {
      "id": "CDEFAULT_RF_20200503120903", 
      "multi_input_uri": "http://localhost:5000/outputs/CDEFAULT_RF_20200503120903", 
      "single_input_uri": "http://localhost:5000/output/CDEFAULT_RF_20200503120903"
    }
  ]
}
```

### 3.2. Getting the prediction for a single record
When sending a single record to a specific model, data must be JSON-formatted as in the example command below. The command
should follow the following pattern:

```bash
curl -H "Content-Type: application/json" -X POST --data <data>  http://localhost:5000/output/<model_id>
```

For example:
```bash
curl -H "Content-Type: application/json" -X POST \
--data '{"checking_balance":"unknown","savings_balance":"unknown","installment_rate":4,"personal_status":"single male","residence_history":1,"installment_plan":"none","existing_credits":1,"dependents":1}' \
http://localhost:5000/output/CDEFAULT_RF_20200503120903
```

The server will return a JSON-formatted response consisting in a simple dictionary, the prediction being the `'probability'`
field. For example the example command above should return: 

```bash
{
  "model_id": "CDEFAULT_RF_20200503120903", 
  "probability": 0.19969359076633833
}
```

**Notice about the prediction**: The prediction can either be a predicted label or the predicted probability to belong to 
the positive class (binary classification). As it seems we would like to be able to compute ROC curves based on the server
responses, this requires to return a probability and not a label. We can also return both and let the client decides which 
one matches its use case. 

### 3.3. Getting the prediction for a batch of records
When sending a batch of record to a specific model, data must be JSON-formatted as in the example command below. The command
should follow the following pattern:

```bash
curl -H "Content-Type: application/json" -X POST --data '{"data":[<record_data_1>, <record_data_2>]}'  http://localhost:5000/outputs/<model_id>
```

For example:
```bash
curl -H "Content-Type: application/json" -X POST \
--data '{"data":[
{"checking_balance":"unknown","savings_balance":"unknown","installment_rate":4,"personal_status":"single male","residence_history":1,"installment_plan":"none","existing_credits":1,"dependents":1},
{"checking_balance":"< 0 DM","savings_balance":"< 100 DM","installment_rate":4,"personal_status":"single male","residence_history":2,"installment_plan":"stores","existing_credits":1,"dependents":2}
]}' \
http://localhost:5000/outputs/CDEFAULT_RF_20200503120903
```

The command should return a JSON-formatted response that consists in a dictionary with a single `'predictions'`  field. The 
latter consists in a list of dictionaries, each containing the prediction for a single record. For example the example 
command above should return:

```bash
{
  "model_id": "CDEFAULT_RF_20200503120903", 
  "predictions": [
    {
      "probability": 0.19969359076633833
    }, 
    {
      "probability": 0.6694665395972683
    }
  ]
}
```

## 4. Possible improvements
From a code quality perspective we would suggest the following improvements: 
* Add unit and integration tests,
* Allow to package the application (add a build script such as a `setup.py`) for easier deployment, 
* Add informative logging,
* Take out the business logic code from the web application code base,
* Increase code modularity/decrease coupling by using factory methods/objects,
* Enhance code documentation by adding docstrings, type hints, complexity analysis where relevant, etc.
* Add a *CHANGELOG.md* file (depends on the versioning policy),
* Improve configuration management.

From a functional perspective, we would suggest the following improvements:
* Add support for other model formats (pickle, etc.)
* Provide more information in the prediction response dictionaries (record ID, label and probability, model metadata) 
* Improve the error handling behavior: make sure we always return a JSON structure, even in case of errors
* Find a more convenient way to upload a batch of data (ex: direct file upload).
 