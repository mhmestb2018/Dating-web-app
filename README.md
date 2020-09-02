# A Dockerized dating app
### Using Flask, MariaDB, Node, React.js and Bootstrap

The frontend is accessible on port 3000 on your machine ([link](http://0.0.0.0:3000)).

### Requirements
- WSL 2 (Windows)
- Docker
- docker-compose (Windows Server/Linux)

## Run
You will need to set up two environment variables in order to send confirmation emails. At this stage, only Gmail addresses are supported.
```bash
export FLASK_GMAIL=mymail@gmail.com
export FLASK_GMAIL_PASSWORD=my_password
export FLASK_HOST='http://0.0.0.0'
docker-compose up
```

## Database
The MariaDB SQL database and user pictures will be stored in local docker volumes.
To reset the database:
```bash
docker volume ls
docker volume rm xxxxx_db-data
docker volume rm xxxxx_user-pictures
```

## Authors
* **Guillaume Madec** @ 42 Lyon
* **Kevin Azoulay** @ 42 Lyon