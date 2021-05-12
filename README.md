# build docker
```
apt-get update && apt-get upgrade
apt-get install sqlite3 libsqlite3-dev
```

# set up docker
Run this application through docker

```
sudo docker run --name liquid -v /"$(pwd)":/home -p 8000-9000:8000-9000 --shm-size=2gb --interactive --tty --rm python:3.9-slim bash
```

Interactive mode
```
sudo docker exect -it liquid bash
```
(note, `liquid` in this command is the name of the docker container specified
in the command above.)

Once inside interactive mode, make sure `FLASK_APP`and `FLASK_ENV` is defined in your session
```
export FLASK_APP=liquid
export FLASK_ENV=development
```

# sqlite
sqlite db commands must be run through docker otherwise you will encounter permission errors

sqlite3 interactive must be run *outside* of docker because it is not installed
in docker container (i think bc of python slim version)

```
sqlite3 instance/liquid.db
```
