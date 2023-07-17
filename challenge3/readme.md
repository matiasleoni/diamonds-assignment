# Challenge 3

> "Francesco likes your model! Now he wants to use it. To improve the model, Francesco is open to hire a new expert and let him value more stones. Create an automatic pipeline capable of training a new instance of your model from the raw dataset."

For this challenge I created two python scripts.

1. The first one, `pipeline_training.py`, reads the csv file `diamonds.csv`, processes the columns "carat", "color" and "clarity" and then trains the model against the ground truth given in the column "price". These transformations and model training are encoded in an object of the `sklearn.pipeline.Pipeline()` class and, after training, the `Pipeline()` object is saved in the `my_pipeline.joblib` file.

2. The second one, `diamond_pricing.py`, is an I/O python script which asks the features of a given diamond and returns the estimated price by using the `Pipeline()` object loaded from the `my_pipeline.joblib` file.

Besides those files, there is the `requirements.txt` which lists the libraries needed for these scripts.

It should be said, regarding the training of the model, that since Francesco and its clients needed a sufficiently simple model to be able to grasp its working, whe chose a model which has an algorithm which cannot learn incrementally. This means that if the expert hired by Francesco values additional diamonds, the model has to be retrained with the combination of old and new data (this can be done by simply appending the new data in the `diamonds.csv` file).
