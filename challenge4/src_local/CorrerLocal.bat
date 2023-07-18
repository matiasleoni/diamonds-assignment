docker build -t fastapi_local_image .

docker create --name fastapi_local_container -v %cd%:/code -host=0.0.0.0 -p 8081:8081 fastapi_local_image tail -f /dev/null

docker start fastapi_local_container

docker exec -it fastapi_local_container bash

echo "uvicorn app.main:app --host 0.0.0.0 --port 8081 --reload"