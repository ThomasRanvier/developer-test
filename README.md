# Giskard developer test

## Cloning the Repository

To clone this repository, use the following command:

```bash
git clone https://github.com/ThomasRanvier/developer-test.git
```

## Using the API and Web application

1. Before you can reproduce this Dockerized project, make sure you have the following prerequisites installed on your system:

- Docker: [Installation Guide](https://docs.docker.com/get-docker/)
- Docker Compose: [Installation Guide](https://docs.docker.com/compose/install/)

2. Build the Docker images and start the containers:

```bash
docker-compose up --build
```

This command will build the Docker images and start the containers defined in the `docker-compose.yml` file. You may need to use `sudo` or run the command with appropriate permissions.

The millenium-falcon.json and universe.db files that the API uses must be placed in the folder "prod_data", which is shared with the server container. Note that you can change those files and request new odds without needing to restart the web service.

3. The project should now be up and running. Access it in your web browser by visiting:

```
http://localhost:8080
```

4. To stop and remove the Docker containers, run:

```bash
docker-compose down
```

## Using the CLI

You can use the CLI with the following command, by replacing N with 1, 2, 3, or 4:
```bash
python give_me_the_odds.py examples/exampleN/millennium-falcon.json examples/exampleN/empire.json
```