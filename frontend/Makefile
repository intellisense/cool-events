# Using $(lastword $(MAKEFILE_LIST)) and -f ... ensures that the $(MAKE) command uses the same makefile,
# even if that makefile was passed with an explicit path (-f ...) when make was originally invoked.
THIS_FILE := $(lastword $(MAKEFILE_LIST))

build:
	docker-compose build

start:
	docker-compose up

eslint:
	docker-compose exec frontend yarn lint

lint:
	@$(MAKE) -f $(THIS_FILE) eslint
