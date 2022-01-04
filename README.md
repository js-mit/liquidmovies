# Liquid Video AKA Wet Frames

## Development
Visit our [setup guide](/SETUP.md) for instructions on setup.

This project uses [Black](https://black.readthedocs.io/en/stable/) and [flake8](https://flake8.pycqa.org/en/latest/) to standard python files

Before committing code:
- run `black .` on the root directory to reformat python files
- run `flake8 .` on the root directory and resolve all issues

> flake8 config can be found in `.flake8` in the root directory

## Deployment

Deploy to lightsail.

### Build container
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


