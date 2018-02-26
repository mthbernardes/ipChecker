# ipChecker
Tool to check if a given IP is a node tor or an open proxy.

# Why?
Sometimes all your throttles are not enough to stop brute force attacks or any kind of massive attacks, so it can help you to drop, some attackers who use tor or open proxies.

# How it works
The ipChecker has some plugins which scrap proxies ips from public sites, all this ip's are stored in a database where you can make consults using the provided API.

Basically, when you run the command ```make run``` it will start docker swarm create one service for the API wich can be escaleted and starts with 4 containers, another service for the updater which is the script responsible to run all the plugins that grab all the proxies and tor nodes,this service starts with only one container, and at last  one container for the mongodb where all data are stored.

The containers communicate through a docker network called ipchecker-network, and only the port 8080 is exposed where you consume the API.

To avoid a lot of false positive, the api only returns ip's from the curent day, because almost proxies servers and tor nodes, are dinamic ip's. 

# Install
```bash
git clone https://github.com/mthbernardes/ipChecker
cd ipchecker/
```

Option to execute the service:
- make buld -> Build all images
- make run -> Build and run all images
- make stop -> Stop all services
- make wipe -> Stop all services and wipe all images and mongodb data

# Basic Usage
Here is the basic usage of the API, for see all the endpoints and access the / endpoint.

| Endpoint        | method           | Description  |
| ------------- |:-------------:| -----:|
| /      | GET | Document of all endpoints |
| /statistics      | GET      | Informations about blocked requests, allowed requests, and number of all proxies on database(per day) |
| /ips?ip=127.0.0.1 | GET | Search for a single IP on database |
| /all | GET      | return all ips on database |


