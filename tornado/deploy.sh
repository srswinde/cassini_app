#!/bin/bash

# deploy
docker build -t registry.digitalocean.com/cassini/tornado-app:latest . 
docker push registry.digitalocean.com/cassini/tornado-app:latest
kubectl rollout restart deployment cassini-app

kubectl get pods | grep Running