# Development

> Run the following commands inside the cloned repo

## Create a user-defined bridge network
A user-defined bridge network allows different containers to talk to each other.
```
sudo docker network create liquid-network
```

## Run redis in a container
We need to run a redis server, connect it to our docker network
```
sudo docker run --name liquid-redis --net liquid-network -d redis
```
> Since our redis container is called `liquid-redis`, make sure to name env variables appropriately, ie. `CELERY_BROKER_URL=redis://liquid-redis:6379/0`

## Create the app container
Run the main application through docker, connect it to the docker network

```
sudo docker run --name liquid-app -v /"$(pwd)":/home -p 8000-8999:8000-8999 --net liquid-network --shm-size=2gb --interactive --tty --rm python:3.9 bash
```

If the container is already running, then you can enter the container using the following command:
```
sudo docker exec -it liquid-app bash
```

## Container setup
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
(You may need to enter the `/home` directory before running this command)

Make sure `FLASK_APP`and `FLASK_ENV` is defined in your session
```
export FLASK_APP=liquid
export FLASK_ENV=development
```

Navigate to where the appplication is (`/home`) and run the app
```
flask run --port 8000 --host=0.0.0.0
```

## Celery

To run celery, enter the liquid-app container and run
```
celery -A celery_worker.celery worker --pool=solo --loglevel=info
```

## Dev standard

This project uses [Black](https://black.readthedocs.io/en/stable/) and [flake8](https://flake8.pycqa.org/en/latest/) to standard python files

Before committing code:
- run `black .` on the root directory to reformat python files
- run `flake8 .` on the root directory and resolve all issues

> flake8 config can be found in `.flake8` in the root directory

## Sqlite
This application will default to using a local instance of sqlite as a database if a DATABASE_URL is not defined as a environment variable.

sqlite db commands must be run through docker otherwise you will encounter permission errors

> sqlite3 interactive must be run *outside* of docker because it is not installed
in docker container (i think bc of python slim version)

```
sqlite3 instance/liquid.db
```

# Deployment

Deploy to lightsail.

## Build container
Run the following command at root dir (`sudo` may be needed)
```
docker build -t liquid .
```

Test that the build works locally (test on localhost:8080)
```
docker run -it --rm -p 8080:8080 liquid
```

Tag your docker image
```
docker tag liquid <username>/liquid
```

Push docker image to dockerhub
```
docker push <username>/liquid
```

Create a "container" on Lightsail. Enter variables in `.env` file as environment variables during container setup.

