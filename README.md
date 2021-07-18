# django3

![example workflow](https://github.com/NeverWalkAloner/django3/actions/workflows/github-actions-demo.yml/badge.svg)

### Start project

Run

```
docker-compose up -d --build
```

Open http://127.0.0.1:8080/swagger/ in the browser and use `Token <token_value>` to authorize.

### Start tests

Run

```
docker-compose exec web python -m pytest
```

### Create superuser and open admin

Run

```
docker-compose exec web python manage.py createsuperuser
```

Open http://127.0.0.1:8080/admin/ in the browser and use superuser username password.
