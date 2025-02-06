# The Cassini Database

## Cassini
Cassini is a sulcata tortoise who lives in my backyard. 

[Cassini](cassini.jpg)

There are many pictures of cassini floating around the internet. Mostly the ones I posted on his [website](https://swahle.org/cassini/detections.html?date=Wed%20Feb%2005%202025).

This app is an attempt to leverage that website to create a database of cassini images in a kubernets cluster. It uses lazy loading and a process server to pull the cassini images from his website and store them in a database managed by a kubernetes cluster.


## Description

This web application runs on a kubernetes cluster hosted by Digital Ocean. It leverages three nodes in a worke pool to host the database and the python api. 

## Postgres Database

The database was built using the kubernetes manifest files found in the [databse](database) directory. [postgres-pvc.yaml](database/postgres-pvc.yaml) creates a persistent volume claim for the database. Appyling this file creates a digital ocean volume so the database can persist. The [postgres-statefulset.yaml](database/postgres-statefulset.yaml) file build a postgres database using the official postgres docker image and gives it access to the peristnat volume. 


## Python API

The python interface to the database and web server source code is found in the [tornado](tornado) directory. 
