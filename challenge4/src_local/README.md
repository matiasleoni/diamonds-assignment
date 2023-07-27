## Local API Dev

This is the local version of the API used to develop it before deployment.

To edit a live version of it you should run the Windows command prompt script `CorrerLocal.bat` with the Docker daemon running. An analogous bash script could easily be rewritten for UNIX systems.

With the container running, in its bash terminal run the command:
```
uvicorn app.main:app --host 0.0.0.0 --port 8081 --reload
```
If one then opens a browser in
```
http://localhost:8081/
```
the root GET of the API should be called with instructions of its use. The API can be edited live since the uvicorn server is running in the --reload mode.