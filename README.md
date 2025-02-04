# Cassini's Web Application


This application is an attempt to create scalable and deployable applications starring my favorite tortoise cassini. Cassini has a lot of data including images and sensor data. THe idea of this application is to share and interact with Cassini's data using modern tools like kubernetes, docker, postges and other tools. 


## First steps: Kubernetes

The first step was to spin up a kubernetes cluster. I chose Digital Ocean as my host


### Create the cluster
To create the cluster, I used the Digital Ocean Create --> Kubernetes Cluster interface. I had a pool of 3 nodes up in about 5 minutes.


### Setup remote access tools
Digital Ocean makes creating the cluster very simple but accessing the nodes remotely take a it more knoweledge. 

The first thing I had to do was install digital oceans api client [doctl](https://docs.digitalocean.com/reference/doctl/) and kubernetes client [kubectl](https://kubernetes.io/docs/reference/kubectl/) on my local linux computer. 

doctl requires an api token to connect to a digital ocean acount. To make that work I cretaed an api key and followed [these instructions](https://docs.digitalocean.com/reference/doctl/how-to/install/)


Once these steps were completed I was able to run kubectl commands to interrogate the state of the cluster like:

```
kubectl cluster-info
kubectl get nodes
kubectl version
```


### Deploy an ingress controller

To handle incoming web connections I used the kubernetes [nginx ingress controller](https://kubernetes.github.io/ingress-nginx/deploy/#quick-start).

### Creating the application




