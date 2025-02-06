# The Cassini Database

## Cassini
Cassini is a sulcata tortoise who lives in my backyard. 

![Cassini](cassini.jpg)

A camera on Cassini’s burrow takes images every minute that post to his [website](https://swahle.org/cassini/detections.html?date=Wed%20Feb%2005%202025). An AI model has been trained to detect Cassini so that his activity can be monitored and we can be alerted when he is out and about and looking for treats. That website is hosted on a bare metal linux server in a cabinet (no way to run enterprise software). 

This app is an attempt to migrate some of his images to a kubernetes cluster that is infintely scalable for cassini's growing user base.


## App Description

This web application runs on a kubernetes cluster hosted by Digital Ocean. It leverages three nodes in a worker pool to host the database and a python api. It uses lazy loading and a process server to pull the cassini images from his website and store them in a database spawned by the cluster. The application has a web interface at [http://cassini.scottswindell.net](http://cassini.scottswindell.net)

## Postgres Database

The database was built using the kubernetes manifest files found in the [databse](database) directory. [postgres-pvc.yaml](database/postgres-pvc.yaml) creates a persistent volume claim for the database. Appyling this file creates a digital ocean volume so the database can persist. The [postgres-statefulset.yaml](database/postgres-statefulset.yaml) file spawns a postgres database using the official postgres docker image and gives it access to the peristnat volume. 


## Python Server and database interface

The python source code is found in the [tornado](tornado) directory. The python source is split into two python packages, the [database](tornado/database) package and the api package [tornado/api](tornado/api). The database package contins the sqlalchemy models and the api package contains the tornado web request handlers and a process server to handle the lazy loading of images from cassini's website into the cloud database. 

## Using the App

Visit the app landing page [here](http://cassini.scottswindell.net). From there you can click the lazy loader to load images or see a list of the processes run previously. 

If you would like to go straight to the lazy loader, you can run it for any data by setting the GET data paramerter `date`. For example [http://cassini.scottswindell.net/lazyload?date=8-23-2024](http://cassini.scottswindell.net/lazyload?date=8-23-2024).


## Testing

Testing is done using pytest and performed on all commits pushed to the repository. The test are located in [tornado/test/test_process_loaders.py](tornado/test/test_process_loaders.py) and the github actions are located in [.github/workflows](.github/workflows).
