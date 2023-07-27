# Challenge 4

> "Finally, Francesco wants to embed your model in a web application, to allow for easy use by his employees. **Develop a REST API to expose the model predictions**."

We have developed an API and deployed it in a dockerized ECS instance of AWS cloud. It can be found in <http://18.234.175.187/>. The API works with a GET request with URL parameters following the structure `http://18.234.175.187/pricing/{carat}/{color}/{clarity}` which responds with a JSON with the features and the price computed from the model developed in the previous challenges. A simple documentation can be found in the root <http://18.234.175.187/> while a more technical one in <http://18.234.175.187/docs>.

The API uses the object of the scikit-learn class `Pipeline()` that was constructed, trained and saved in the file `my_pipeline.joblib` in the previous challenge. 

The contents of this directory:
* Folder `src` has the Dockerfile and the API code that can be found together with the PIP `requirements.txt` libraries to be installed on top of a `python:3.9-slim-bullseye` system. This is all the code deployed in the AWS ECS instance. 
* The `src_local` folder on the other hand, contains the code used to develop the API in a local Docker container before cloud deployment. In it, another [README.md](src_local/README.md) file can be found explaining its use.
* The file `API_testing.py` is a script to make some tests of the API responses and the `requirements.txt` found in this folder contains the libraries needed for this testing to work.