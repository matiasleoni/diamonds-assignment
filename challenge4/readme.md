# Challenge 4

> "Finally, Francesco wants to embed your model in a web application, to allow for easy use by his employees. Develop a REST API to expose the model predictions."

I have developed an API and deployed it in a dockerized ECS instance of AWS cloud. It can be found in <http://18.234.46.13/>. The API works with a GET request with URL parameters following the structure `http://18.234.46.13/pricing/{carat}/{color}/{clarity}` which responds with a JSON with the features and the price computed from the model developed in the previous challenges. A simple documentation can be found in the root <http://18.234.46.13/> while a more technical one in <http://18.234.46.13/docs>.

In the directory `src` the Dockerfile and the API code con be found togheter with the PIP `requirements.txt` libraries to be installed on top of a `python:3.9-slim-bullseye` system. The `src_local` directory on the other hand, contains the code used to develop de API locally before cloud deployment. The API uses the object of the scikit-learn class `Pipeline()` that was saved in the file `my_pipeline.joblib`.