# A Dockerized dating app
### Using Flask, MariaDB, Node, React.js and Bootstrap

The frontend is accessible on port 3000 on your machine ([link](http://0.0.0.0:3000)).
For test purposes, you can query mySQL on port 32000.

## Setup
### Requirements
- WSL 2 (Windows)
- Docker
- docker-compose (Windows Server/Linux)
You will set two environment variables in order to send confirmation emails. At this stage, only Gmail addresses are supported.
Create/manage your Google Account application passwords on [Google App Passwords page](https://myaccount.google.com/apppasswords).
These variables should be set or specified in a *.env* file.
The local.env file will not be tracked by git afterwards.
```bash
 echo "FLASK_GMAIL=XXXX@gmail.com
FLASK_GMAIL_PASSWORD=XXXX" >> config/local.env
git update-index --assume-unchanged config/local.env
```

### Build (optional)
All docker images will be built during the first launch of the stack. In case you just want to build the images for now, or to rebuild after dependancies changes (Dockerfiles, back/requirement.txt, front/packages.json):
```bash
docker-compose build
```

## Run
```bash
docker-compose up
```

## Database
MariaDB data and user pictures will be stored in local docker volumes.
To reset the database and/or clear pictures storage:
```bash
docker-compose down -v
```

## Uninstall
To delete all user data and docker images
```bash
docker-compose down -v --rmi all
```

## Authors
* **Guillaume Madec** @ 42 Lyon
* **Kevin Azoulay** @ 42 Lyon