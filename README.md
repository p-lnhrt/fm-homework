##### Author: Pierre LIENHART
##### Contact: pierre.lienhart[at]gmail.com

# FairMoney Machine Learning Engineer homework
This homework consist in two exercises named "training" and "deployment". Each exercise is associated with a dedicated 
directory and documentation (*README.md* file).

## 1. Requirements
This homework has been developed using:
* [Conda](https://docs.conda.io/en/latest/) package manager (version 4.6.11)
* [Python](https://www.python.org/downloads/) (version 3.6.8)

We also provide a dedicated *requirements.txt* file to set up the appropriate runtime environment. 

## 2. Execution environment
To ensure our project runs using the appropriate dependencies, we first create and activate a dedicated Python (virtual)
execution environment using the project's *requirements.txt* file. Change your current directory to the projects's root 
directory and run the following commands:

```bash
conda create -y -c conda-forge -n py36-fm --file requirements.txt
```

Activate the environment using:

```bash
conda activate py36-fm
```

If the above command requires extra `conda` configurations, you can still use:

```bash
source activate /opt/anaconda/envs/py36-fm
```

Starting from this moment, **we always assume that the current Python execution environment is the project's dedicated
virtual environment**.
