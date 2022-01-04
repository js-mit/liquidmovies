# Development

There are two ways to run the application for development purposes:
- Docker-compose (recommended)
- Managing docker containers manually

Before running either, make sure the `.env` file is filled out and placed into the root directory.

## Docker-compose (recommended)

> This method requires that docker-compose is installed on your development machine

Run the following code in the root directory of the cloned repo:
```
sudo docker-compose up
```
> All docker configurations are listed out in the `docker-compose.yaml` file in the root directory

Since the files in your local directory are mounted onto the docker containers, editting local files will take effect without having to restart the docker compose.

To stop your development environment, <ctrl-c> to escape. Run the following to stop and remove containers, networks, volume, etc:
```
sudo docker-compose down
```

> If a docker-compose error occurs, try restarting with `sudo docker-compose restart`


## Managing docker containers manually

This method may be preferable for debugging individual elements of the docker compose architecture.

Run the following commands inside the cloned repo.

### 1. Create a user-defined bridge network
A user-defined bridge network allows different containers to talk to each other.
```
sudo docker network create liquid-network
```

### 2. Run redis in a container
We need to run a redis server, connect it to our docker network
```
sudo docker run --name liquid-redis --net liquid-network -d redis
```
> Since our redis container is called `liquid-redis`, make sure to name env variables appropriately, ie. `CELERY_BROKER_URL=redis://liquid-redis:6379/0`

### 3. Create the flask app container
Run the main application through docker, connect it to the docker network

```
sudo docker run --name liquid-app -v /"$(pwd)":/home -p 8000-8999:8000-8999 --net liquid-network --shm-size=2gb --interactive --tty --rm python:3.9 bash
```

If the container is already running, then you can enter the container using the following command:
```
sudo docker exec -it liquid-app bash
```

### 4. Flask app container setup
Once inside the `liquid-app` container, we need to install some basic libraries
```
apt-get -y update && apt-get -y upgrade
apt-get -y install sqlite3 libsqlite3-dev
apt-get -y install ffmpeg libsm6 libxext6
```

Install flask and other requirements
```
pip install -r requirements.txt
```
(You may need to enter the `/app` directory before running this command)

Make sure `FLASK_APP`and `FLASK_ENV` is defined in your session
```
export FLASK_APP=liquid
export FLASK_ENV=development
```

Navigate to where the appplication is (`/app`) and run the app
```
flask run --port 8000 --host=0.0.0.0
```

### 5. Sqlite
This application will default to using a local instance of sqlite as a database if a DATABASE_URL is not defined as a environment variable.

sqlite db commands must be run through docker otherwise you will encounter permission errors

> sqlite3 interactive must be run *outside* of docker because it is not installed in docker container (i think bc of python slim version)

```
sqlite3 instance/liquid.db
```

### 6. Celery

To run Celery, enter the liquid-app container and run:
```
celery -A celery_worker.celery worker --pool=solo --loglevel=info
```
> It is suggested that the celery worker is kicked off before the `flask run` command is called


To run Celery Beat, enter the liquid-app container and run:
```
celery -A celery_worker.celery beat --loglevel=info
```

To monitor Celery tasks, run Flower inside the liquid-app container as well:
```
celery -A celery_worker.celery flower --address=0.0.0.0 --port=8001
```
