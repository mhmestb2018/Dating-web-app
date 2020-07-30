# A Dockerized Flask dating app
### Using Flask, SQLAlchemy and Bootstrap

As I was working on the API side of things, don't expect too much of the frontend, mostly here as an user-friendly way to test the beast.

Everything is served on port 5000 on your machine ([link](http://0.0.0.0:5000)).

### Requirements
- Docker
- docker-compose

## Run
```bash
docker-compose up
```

## Database
The MariaDB SQL database will be created in a local docker volume.
To reset the database, while in this folder:
```bash
docker volume rm matcha_db-data
```
