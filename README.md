# build docker
```
apt-get install sqlite3
```

# set up 
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

make sure `FLASK_APP`and `FLASK_ENV` is defined in your session
```
export FLASK_APP=liquid
export FLASK_ENV=development
```
