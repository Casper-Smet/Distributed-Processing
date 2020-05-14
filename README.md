# Distributed-Processing
GitHub Repo for the course Distributed Processing for the bachelor programma Artificial Intelligence at the Utrecht University of Applied Sciences Utrecht.

## Data location
All data must be placed in `input` folder at the root of this project.

## Date output
All output data will be placed in the `output` folder at the root of this project.

# Used models
For this assignment, we implemented a Decision Tree Regressor, a Random Forest Regressor, and an LSTM based neural network. After laborious testing, the best performing regressor was the Random Forest Regressor.

The initial data exploration and model planning can be found in `Assignment_1/Flickbike_data_analysis.ipynb`. The predictive models can be found in `Assignment_2/`, with our final model being `Assignment_2/RandomForestRegressor.ipynb`.

In order to run these notebooks, follow these instructions: 

* Install requirements.txt
* Install TensorFlow-Keras
* place the following files into `input/`
  * `bikes.csv`
  * `Nationale Feestdagen.csv` (see `Assignment_1/Flickbike_data_analysis.ipynb`)
  * `train.csv`
  * `test.csv`
  * `sampleSubmission.csv`
* run the notebook `Flickbike Dataprep.ipynb`