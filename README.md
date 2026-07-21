# passwordGeneratorXKCD

A web-based password generator inspired by the classic [XKCD "Password Strength" comic](https://xkcd.com/936/), which demonstrates that passwords like `correct horse battery staple` are both more secure and easier to remember than complex but shorter passwords.

## Purpose

This application provides a Flask-based web interface that generates secure, memorable passwords using random words. Rather than creating hard-to-remember strings like `Tr0ub4dor&3`, it generates easy-to-remember passphrases using the XKCD method - combining random common words with optional delimiters and capitalization.

Users are presented with multiple password options to choose from, making it easy to find one that's both secure and memorable.

## Running with Docker

The easiest way to run this application is using Docker Compose:

```yaml
services:
  password-generator:
    container_name: password-generator
    restart:  unless-stopped
    image: ghcr.io/main-roads/passwordgeneratorxkcd:${DOCKER_TAG:-latest}
    volumes:
      - ./config.yaml:/home/xkcd/web/project/config.yaml:ro # Optional, for overriding defaults
    read_only: true
    tmpfs:
      - /tmp
```

```bash
docker compose up -d
```

This will:
- Pull the latest image from `ghcr.io/main-roads/passwordgeneratorxkcd`
- Start the password generator service
- Run the container with read-only filesystem for security

To use a specific version, set the `DOCKER_TAG` environment variable:

```bash
DOCKER_TAG=v1.0.0 docker compose up -d
```

To stop the service:

```bash
docker compose down
```

## Configuration

The application can be configured using `config.yaml`. Key settings include:

- **numwords**: Number of words per password (default: 4)
- **min_length/max_length**: Word length constraints (default: 4-7 characters)
- **delimiter**: Character(s) between words
- **random_delimiters**: Use random delimiters from valid_delimiters
- **case_methods**: Capitalization style (e.g., "capitalize")
- **count**: Number of passwords to generate (default: 25)

See `config.yaml` for all available options.
