COMPOSE=docker compose -f srcs/docker-compose.yml
MKDIR=mkdir -p
RM=rm -rf

.PHONY: all build clean down follow logs ps re rebuild restart

all:
	$(COMPOSE) up -d

bonus:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

build:
	$(COMPOSE) build --no-cache

refresh:
	$(COMPOSE) build

logs:
	$(COMPOSE) logs

follow:
	$(COMPOSE) logs --follow

ps:
	$(COMPOSE) ps

edit:
	vim srcs/docker-compose.yml

clean:
	sudo $(RM) $(HOME)/data

re: down clean build all follow

rebuild: down refresh all follow

restart: down all follow
