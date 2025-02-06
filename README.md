# The Cassini Database

## Cassini
Cassini is a sulcata tortoise who lives in my backyard. 

[Cassini](cassini.jpg)

There are many pictures of cassini floating around the internet. Mostly the ones I posted on his [website](https://swahle.org/cassini/detections.html?date=Wed%20Feb%2005%202025). That website is hosted on a bare metal linux server in a cabinet -- no way to run enterprise software. 

This app is an attempt to migrate some of his website to a kubernetes cluster that is infintely scalable for cassini's user base. 


## App Description

This web application runs on a kubernetes cluster hosted by Digital Ocean. It leverages three nodes in a worker pool to host the database and the python api. It uses lazy loading and a process server to pull the cassini images from his website and store them in a database managed by a kubernetes cluster. The application has a web interface at [http://cassini.scottswindell.net](http://cassini.scottswindell.net)

## Postgres Database

The database was built using the kubernetes manifest files found in the [databse](database) directory. [postgres-pvc.yaml](database/postgres-pvc.yaml) creates a persistent volume claim for the database. Appyling this file creates a digital ocean volume so the database can persist. The [postgres-statefulset.yaml](database/postgres-statefulset.yaml) file build a postgres database using the official postgres docker image and gives it access to the peristnat volume. 


## Python API

The python interface to the database and web server source code is found in the [tornado](tornado) directory. 
