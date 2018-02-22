NETWORK_NAME="ipchecker-network"
BASE_DIR="$(HOME)/.ipchecker"
MONGO_VOLUME="$(BASE_DIR)/mongo"
API_IMAGE="g4mbl3r/ipchecker-api"
UPDATER_IMAGE="g4mbl3r/ipchecker-updater"

api/build:
	cd api/ && docker build -t $(API_IMAGE) .

updater/build:
	cd updater/ && docker build -t $(UPDATER_IMAGE) .

api/run:
	docker service create --replicas 4 --name ipchecker-api -p 8080:8080 --network=$(NETWORK_NAME) $(API_IMAGE)

updater/run:
	docker service create --replicas 1 --name ipchecker-updater --network=$(NETWORK_NAME) $(UPDATER_IMAGE)

mongo/run:
	docker run --network=$(NETWORK_NAME) -v $(MONGO_VOLUME):/data/db --name mongodb -d mongo

network:
	docker network create $(NETWORK_NAME) -d overlay --opt encrypted --attachable

prepare:
	mkdir -p $(MONGO_VOLUME)
	docker swarm init

wipe: stop
	docker image rm -f $(API_IMAGE) $(UPDATER_IMAGE) mongo
	sudo rm -rf "$(BASE_DIR)"

stop:
	-docker service rm ipchecker-api
	-docker service rm ipchecker-updater
	-docker rm -f mongodb
	-docker network rm $(NETWORK_NAME)
	-docker swarm leave --force

build: api/build updater/build

run: build prepare network mongo/run updater/run api/run

.PHONY: build
