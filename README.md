# Cool Events

A simple application created using **[Python](https://www.python.org/)**, **[Django](https://www.djangoproject.com/)**, **[Django REST Framework](https://www.django-rest-framework.org/)**, **[Dj REST Auth](https://dj-rest-auth.readthedocs.io/en/latest/index.html)** & **[Vue](https://vuejs.org/)** (with webpack hot reload).

## Installation

Development environment is set up via [Docker](https://www.docker.com/) using [Docker Compose](https://docs.docker.com/compose/).

### API

```bash
cd api
make build
make start
```

You should now be able to access the API running on [http://0.0.0.0:8000](http://0.0.0.0:8000). Visit admin panel at [http://0.0.0.0:8000/admin/](http://0.0.0.0:8000/admin/) to make sure it is accessible.

### Frontend

```bash
cd frontend
make build
make start
```

You should now be able to access the application running on [http://localhost:8080](http://localhost:8080).

## Testing
For running the api tests, run the following command:

```bash
cd api
make test
```

## Linting
### API

For python various tools are used for linting:
- [flake8](https://github.com/PyCQA/flake8)
- [isort](https://github.com/PyCQA/isort)
- [black](https://github.com/psf/black)

First change directory to `api`:
```bash
cd api
```

Use following commands to execute each of the linter:
- `make flake8`
- `make isort`
- `make black`

or run the following command to run all linters:
```bash
make lint
```

See [Makefile](./api/Makefile) for more helpful commands.

### Frontend

Frontend linting is handled by [eslint](https://eslint.org/).
First change directory to `frontend`:
```bash
cd frontend
```
then:
```bash
make eslint
```

or run the following command to run all linters:
```bash
make lint
```

See [Makefile](./frontend/Makefile) for more helpful commands.

## Helping Material

 - [Python](https://docs.python.org/3/)
 - [Django](https://docs.djangoproject.com/en/2.2/)
 - [Django REST Framework](https://www.django-rest-framework.org/)
 - [Vue js](https://vuejs.org/v2/guide/)
 - [Vuex](https://vuex.vuejs.org/)
 - [Vuetify js](https://vuetifyjs.com/en/)
