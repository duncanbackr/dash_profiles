# Template

### Getting Started

Create [.env](.env) as per [.env.example](.env.example) <br>

### Useful commands

`docker-compose build` builds the container <br>
`docker-compose up` starts the container <br>
`docker-compose down` stops the container <br>
`pytest` runs tests <br>
`python manage.py [command]` runs a cli commands found in [manage.py](manage.py) <br>


connect to db
./cloud_sql_proxy -instances=backr-dev:us-central1:data-main=tcp:5432
