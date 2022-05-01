# Using $(lastword $(MAKEFILE_LIST)) and -f ... ensures that the $(MAKE) command uses the same makefile,
# even if that makefile was passed with an explicit path (-f ...) when make was originally invoked.
THIS_FILE := $(lastword $(MAKEFILE_LIST))

build:
	docker-compose build

start:
	docker-compose up

flake8:
	docker-compose exec api flake8 .

isort:
	docker-compose exec api isort .

black:
	docker-compose exec api black .

test:
	docker-compose exec api pytest

shell: # Access the Django Shell on the container
	docker-compose exec api ./manage.py shell

migrate: # Run migrations
	docker-compose exec api ./manage.py migrate

migrations: # Generate migration files
	docker-compose exec api ./manage.py makemigrations

createsuperuser: # Create django super user
	docker-compose exec api ./manage.py createsuperuser

flush:  # Flush all database
	docker-compose exec api ./manage.py flush --noinput

resetdb: # Reset the database, run migrations
	@$(MAKE) -f $(THIS_FILE) flush
	@$(MAKE) -f $(THIS_FILE) migrate

setup_test_data: # Generates dummy data
	docker-compose exec api ./manage.py setup_test_data --confirm

lint:
	@$(MAKE) -f $(THIS_FILE) isort
	@$(MAKE) -f $(THIS_FILE) flake8
	@$(MAKE) -f $(THIS_FILE) black
