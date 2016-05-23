system_dependencies_dev:
	sudo apt-get install graphviz libgraphviz-dev graphviz-dev python-pygraphviz

system_dependencies:
	apt-get install gettext

update:
	workon massificados
	pip install --upgrade pip & pip install -U -r src/requirements.txt

graph:
	rm -f massificados.png
	../env/bin/python2.7 manage.py graph_models -a -g -o  massificados.png



run:
	src/manage.py runserver

migrate:
	workon massificados & src/manage.py migrate

install:
	./scripts/install.sh
	mkvirtualenv massificados & pip install -r src/requirements.txt
	make migrate

resetdb:
	dropdb -U massificados massificados
	createdb -U massificados --owner massificados --encoding "UTF-8" massificados
	rm -rf src/*/migrations/000*
	rm -rf src/*/migrations/001*
	workon massificados & python src/manage.py makemigrations
	workon massificados & python src/manage.py migrate
	workon massificados & python src/manage.py create_default
	workon massificados & python src/manage.py reset_pswd
