[![PyPI version](https://badge.fury.io/py/sentimentanalyser.svg)](https://badge.fury.io/py/sentimentanalyser)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![HitCount](http://hits.dwyl.io/ashhadulislam/sentiment-analyser-lib.svg)](http://hits.dwyl.io/ashhadulislam/sentiment-analyser-lib)
![PyPI - Downloads](https://img.shields.io/pypi/dm/sentimentanalyser.svg)
# sentiment-analyser-lib

### Installation
Use below command to use install 
`pip install sentimentanalyser`

### Usage
New version Supports the following libraries:

1. Nearest Neighbors
2. Linear SVM
3. RBF SVM 
4. Decision Tree
5. Random Forest
6. Neural Net
7. Naive Bayes

For training the model

Provide the file path where data is available
```
from sentimentanalyser import train

# Path to training data and output
filePath="/path_to_data/twitter_train.csv"
outputDir="/path_to_output/outputs"

trainObj=train.Train()
trainObj.train_file_model(filePath,outputDir)
```

```
# For test data
from sentimentanalyser import test
testText=""
test_file_name="/path_to_testdata/twitter_test.csv"
test_reference_file="twitter_train"
outputDir="/path_to_output/outputs"
testObj=test.TestData()

testedDataFrame=testObj.test_model(testText,test_file_name,test_reference_file,outputDir)
```
```
from sentimentanalyser import test
testText=""
test_file_name="/path_to_testdata/bbc_test.csv"
test_reference_file="bbc_train"
outputDir="/path_to_output/outputs"
testObj=test.TestData()
testedDataFrame=testObj.test_model(testText,test_file_name,test_reference_file,outputDir)
```
### Using package in Flask and Django application
This package can be easily integrated and used as a library in your in Django application. This will avoid complexity of managing machine learning workflows with web application. Data sets can be uploaded from UI also.

Go to project feedprocessor
Run: python manage.py runserver
Upload training dataset at
`http://localhost:8000/sentiment/models/train/`

Then test with your dataset at
`http://localhost:8000/sentiment/models/test/`
