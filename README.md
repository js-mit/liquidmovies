# set up docker
Run this application through docker container
```
sudo docker run --name liquid -v /"$(pwd)":/home -p 8000-8009:8000-8009 --shm-size=2gb --interactive --tty --rm python:3.9 bash
```

In a seperate terminal, you can also enter the container via this command: 
```
sudo docker exec -it liquid bash
```
(note, `liquid` in this command is the name of the docker container specified
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

# sqlite
sqlite db commands must be run through docker otherwise you will encounter permission errors

sqlite3 interactive must be run *outside* of docker because it is not installed
in docker container (i think bc of python slim version)

```
sqlite3 instance/liquid.db
```
