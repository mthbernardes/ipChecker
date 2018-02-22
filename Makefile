NETWORK_NAME="ipchecker-network"

api/build:
	cd api/ && docker build -t g4mbl3r/ipchecker-api .

updater/build:
	cd updater/ && docker build -t g4mbl3r/ipchecker-updater .

api/run:
	docker service create --replicas 4 --name ipchecker-api -p 8080:8080 --network=$(NETWORK_NAME) g4mbl3r/ipchecker-api

updater/run:
	docker service create --replicas 1 --name ipchecker-updater --network=$(NETWORK_NAME) g4mbl3r/ipchecker-updater

mongo/run:
	docker run --network=$(NETWORK_NAME) --name mongodb -d mongo

network:
	docker network create $(NETWORK_NAME) -d overlay --opt encrypted --attachable

prepare:
	docker swarm init

stop:
	docker service rm ipchecker-api
	docker service rm ipchecker-updater
	docker rm -f mongodb
	docker network rm $(NETWORK_NAME)
	docker swarm leave --force

build: api/build updater/build

run: build prepare network mongo/run updater/run api/run

.PHONY: build
