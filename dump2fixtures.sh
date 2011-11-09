#!/bin/bash


echo Dumping Auth
python manage.py dumpdata --format=yaml auth > auth_fix/fixtures/initial_data.yaml


echo Dumping Beers
python manage.py dumpdata --format=yaml beers > beers/fixtures/initial_data.yaml

echo Dumping Billboards
python manage.py dumpdata --format=yaml billboard > billboard/fixtures/initial_data.yaml
