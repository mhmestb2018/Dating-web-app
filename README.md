# A Dockerized dating app
### Using Flask, MariaDB, Node, React.js and Bootstrap

The frontend is accessible on port 3000 on your machine ([link](http://0.0.0.0:3000)).

### Requirements
- WSL 2 (Windows)
- Docker
- docker-compose (Windows Server/Linux)

## Run
You will need to set up two environment variables in order to send confirmation emails. At this stage, only Gmail addresses are supported.
Create/manage your Google Account application passwords on [Google App Passwords page](https://myaccount.google.com/apppasswords).
These variables should be set or specified in a *.env* file.
```bash
 echo "FLASK_GMAIL=XXXX@gmail.com
FLASK_GMAIL_PASSWORD=XXXX" >> config/local.env
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