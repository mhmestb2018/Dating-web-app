# A Dockerized dating app
### Using Flask, MariaDB, Node, React.js and Bootstrap

Everything is served on port 5000 on your machine ([link](http://0.0.0.0:3000)).

### Requirements
- WSL 2 (Windows)
- Docker
- docker-compose (Windows Server/Linux)

## Run
```bash
docker-compose up
```

## Database
The MariaDB SQL database will be created in a local docker volume.
To reset the database:
```bash
docker volume rm matcha_db-data
```
