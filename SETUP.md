# Development

## Create the container
Run this application through docker

```
sudo docker run --name dev-liquid -v /"$(pwd)":/home -p 8000-8999:8000-8999 --shm-size=2gb --interactive --tty --rm python:3.9 bash
```

## Interactive mode
```
sudo docker exec -it dev-liquid bash
```
(note, `dev-liquid` in this command is the name of the docker container specified
in the command above.)

Once inside interactive mode, we need to install some basic libraries
```
apt-get update && apt-get upgrade
apt-get install sqlite3 libsqlite3-dev
```

Install flask and other requirements
```
pip install -r requirements.txt
```

Make sure `FLASK_APP`and `FLASK_ENV` is defined in your session
```
export FLASK_APP=liquid
export FLASK_ENV=development
```

Navigate to where the appplication is (`/home`) and run the app
```
flask run --port 8000 --host=0.0.0.0
```

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

