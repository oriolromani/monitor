# Fingerprint monitoring service
It is a web service that provides storage of songs plays in radio stations. It is written in python3 using the django
rest framework and uses a PostgreSQL database. Support for docker is also provided to facilitate deploying on production.

## Running the server with docker
To run it with docker just follow this steps:

1. Install [docker](https://docs.docker.com/engine/installation/)
2. Install [docker-compose](https://docs.docker.com/compose/install/)
3. Run the following command:
```
    docker-compose up
```

## Running the test script
Open a new terminal on the same directory.
The script has to be run with python3, so be sure you have it [installed](http://docs.python-guide.org/en/latest/starting/install3/linux/) on your machine.
To minimize the problems of dependencies and versions, we will take advantage of python's
[virtualenv](http://virtualenv.readthedocs.org/en/latest/index.html) tool to create isolated Python environments.
Follow [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html#installation)'s installation guide.
Once installed run:

    virtualenv -p python3 _environment_name_

And then activate it on your shell by:

    source _environtment_name_/bin/activate

Install the requirements for the script by running:

    pip install -r requirements_script.txt

Run the script to test the service:

    python test.py --add-data

## In case you wouldn't like to use Docker
To run the server without using docker you should first create a python3 virtualenv as explained before and install the
requirements of the project by running:

    pip install -r requirements.txt

Then you would have to [install](https://linode.com/docs/databases/postgresql/how-to-install-postgresql-on-ubuntu-16-04/)
PostgreSQL and create a DB like:
```
   sudo -i -u postgres
   createdb bmat
```

Then you would have to migrate the django models to the DB by running:

    python manage.py migrate

And finally run the server by:

    python manage.py runserver
