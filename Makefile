system_dependencies_dev:
	sudo apt-get install graphviz libgraphviz-dev graphviz-dev python-pygraphviz

system_dependencies:
	apt-get install gettext

update:
	workon massificados
	pip install --upgrade pip & pip install -U -r requirements.txt

graph:
	rm -f massificados.png
	workon massificados & python manage.py graph_models -a -g -o  massificados.png



run:
	python manage.py runserver

migrate:
	workon massificados & manage.py migrate

install:
	./scripts/install.sh
	mkvirtualenv massificados & pip install -r requirements.txt
	make migrate

resetdb:
	dropdb  massificados
	createdb  --owner massificados --encoding "UTF-8" massificados
	rm -rf */migrations/000*
	rm -rf */migrations/001*
	workon massificados & python manage.py makemigrations
	workon massificados & python manage.py migrate
	workon massificados & python manage.py create_default
	workon massificados & python manage.py reset_pswd
