#!/bin/bash


if [[ $1 = 'app' ]]; then
    ./dmanage.py startapp --template app_template $2
    exit 1
fi

if [[ $1 = 'run' ]]; then
    ./dmanage.py runserver 0.0.0.0:8000
    exit 1
fi

if [[ $1 = 'migrate' ]]; then
    ./dmanage.py makemigrations
    ./dmanage.py migrate
    exit 1
fi

if [[ $1 = 'gql' ]]; then
    ./dmanage.py graphql_schema --indent 2
    exit 1
fi

if [[ $1 = 'su' ]]; then
    ./dmanage.py createsuperuser
    exit 1
fi

if [[ $1 = 'local' ]]; then
    cat config/local_settings.example > config/local_settings.py
    exit 1
fi

if [[ $1 = 'pip' ]]; then
    pip install -r requirements.txt
    rm -f .devcontainer/requirements.txt
    cat requirements.txt > .devcontainer/requirements.txt
    exit 1
fi

./dmanage.py $@
