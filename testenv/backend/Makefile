create-db:
	PGPASSWORD=${POSTGRES_PASSWORD} psql -h postgres -d postgres -U postgres -c "CREATE USER ${DJANGO_DATABASE_USER} WITH CREATEDB PASSWORD '${DJANGO_DATABASE_PASSWORD}';" || true
	PGPASSWORD=${POSTGRES_PASSWORD} psql -h postgres -d postgres -U ${DJANGO_DATABASE_USER} -c "CREATE DATABASE ${DJANGO_DATABASE_NAME};" || true
	PGPASSWORD=${POSTGRES_PASSWORD} psql -h postgres -d postgres -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ${DJANGO_DATABASE_NAME} TO ${DJANGO_DATABASE_USER};"

init-dev: create-db pip-compile install
	python manage.py migrate
	python manage.py createsuperuser --noinput || true

install:
	pip install -r requirements.dev.txt

pgcli:
	pgcli `python manage.py sqldsn --quiet --style=uri`

pip-compile:
	pip-compile requirements.base.in -o requirements.base.txt
	pip-compile requirements.dev.in -o requirements.dev.txt

run-server:
	python manage.py runserver 0.0.0.0:8000
