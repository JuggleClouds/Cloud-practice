# PostgreSQL docker image based on Alpine Linux

This repository builds a docker image that accepts the same env vars as the
[official postgres build](https://registry.hub.docker.com/_/postgres/) but
with a much smaller footprint. It achieves that by basing itself off the tiny
official alpine linux image.

## Why?

```bash
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
alpine-postgres     latest              b98ff96bb65a        About an hour ago   30.82 MB
alpine              latest              70c557e50ed6        5 weeks ago         4.798 MB
percona             latest              70588d0c4cd4        4 weeks ago         308.6 MB
postgres            latest              6d6a71f8528e        4 weeks ago         265.1 MB
```

# Build

```bash
$ make build
```

# DockerHub

This image is published on DockerHub as `docker pull kiasaki/alpine-postgres`.

[Click here to see it's DockerHub homepage](https://hub.docker.com/r/kiasaki/alpine-postgres/)

# Usage

This image works in the same way the official `postgres` docker image work.

It's documented on DockerHub in it's README: [https://hub.docker.com/_/postgres/](https://hub.docker.com/_/postgres/).

For example, you can start a basic PostgreSQL server, protected by a password,
listening on port 5432 by running the following:

```
$ docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d kiasaki/alpine-postgres
```

Next, you can start you app's container while **linking** it to the PostgreSQL
container you just created giving it access to it.

```
$ docker run --name some-app --link some-postgres:postgres -d application-that-uses-postgres
```

Your app will now be able to access `POSTGRES_PORT_5432_TCP_ADDR` and `POSTGRES_PORT_5432_TCP_PORT` environment variables.

# License

MIT. See `LICENSE` file.
