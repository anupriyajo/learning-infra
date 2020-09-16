# Python CRUD

## Creating virtual environment
`mkdir  ~/.virtualenvs`

`python3 -m venv ~/.virtualenvs/server`

## Selecting virtual environment 
`source ~/.virtualenvs/server/bin/activate`

## Starting postgres docker
`docker run -it -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_USER=py -e POSTGRES_DB=users --rm --name postgres_db postgres:alpine`
