# Everything runs in Docker. Local:  make up      Server:  make deploy APP_ENV=develop IMAGE_TAG=<sha>
APP_ENV ?= local
USE_GPU ?= false
SERVICE ?=

ifeq ($(APP_ENV),local)
OVERLAY := -f docker/docker-compose.dev.yml
else ifeq ($(USE_GPU),true)
OVERLAY := -f docker/docker-compose.gpu.yml
else
OVERLAY :=
endif

COMPOSE := docker compose -p nlr-$(APP_ENV) --env-file env/$(APP_ENV)/infra.env \
	-f docker/docker-compose.yml $(OVERLAY)

.DEFAULT_GOAL := help
.PHONY: help config build up deploy down ps logs logs-tail lint test

help:          ## list the targets
	@grep -E '^[a-z-]+: .*##' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "  %-12s %s\n", $$1, $$2}'

config:        ## print the resolved compose config (contains secrets)
	$(COMPOSE) config

build:         ## build the app images from source (local)
	$(COMPOSE) build

up:            ## local: build and start the whole stack
	$(COMPOSE) up -d --build

deploy:        ## server: pull IMAGE_TAG and restart the stack
	$(COMPOSE) pull
	$(COMPOSE) up -d --remove-orphans

down:          ## stop the stack (volumes are kept)
	$(COMPOSE) down

ps:            ## container status
	$(COMPOSE) ps

logs:          ## follow logs, optionally SERVICE="user_api worker"
	$(COMPOSE) logs -f --tail=100 $(SERVICE)

logs-tail:     ## last log lines, does not follow
	$(COMPOSE) logs --tail=80 $(SERVICE)

lint:          ## ruff + mypy
	ruff check . && ruff format --check . && mypy app core

test:          ## unit tests
	pytest tests
