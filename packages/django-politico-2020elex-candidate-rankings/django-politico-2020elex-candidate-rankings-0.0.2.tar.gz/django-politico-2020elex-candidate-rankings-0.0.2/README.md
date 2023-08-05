![POLITICO](https://rawgithub.com/The-Politico/src/master/images/logo/badge.png)

# django-politico-2020elex-candidate-rankings

### Quickstart

1. Install the app.

  ```
  $ pip install django-politico-2020elex-candidate-rankings
  ```

2. Add the app to your Django project and configure settings.

  ```python
  INSTALLED_APPS = [
      # ...
      'rest_framework',
      'rankings',
  ]

  #########################
  # rankings settings

  RANKINGS_SECRET_KEY = ''
  RANKINGS_AWS_ACCESS_KEY_ID = ''
  RANKINGS_AWS_SECRET_ACCESS_KEY = ''
  RANKINGS_AWS_REGION = ''
  RANKINGS_AWS_S3_BUCKET = ''
  RANKINGS_CLOUDFRONT_ALTERNATE_DOMAIN = ''
  RANKINGS_S3_UPLOAD_ROOT = ''
  ```

### Developing

##### Running a development server

Developing python files? Move into example directory and run the development server with pipenv.

  ```
  $ cd example
  $ pipenv run python manage.py runserver
  ```

Developing static assets? Move into the pluggable app's staticapp directory and start the node development server, which will automatically proxy Django's development server.

  ```
  $ cd rankings/staticapp
  $ gulp
  ```

Want to not worry about it? Use the shortcut make command.

  ```
  $ make dev
  ```

##### Setting up a PostgreSQL database

1. Run the make command to setup a fresh database.

  ```
  $ make database
  ```

2. Add a connection URL to the `.env` file.

  ```
  DATABASE_URL="postgres://localhost:5432/rankings"
  ```

3. Run migrations from the example app.

  ```
  $ cd example
  $ pipenv run python manage.py migrate
  ```
