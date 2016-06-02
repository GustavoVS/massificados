system_dependencies_dev:
	sudo apt-get install graphviz libgraphviz-dev graphviz-dev python-pygraphviz

system_dependencies:
	apt-get install gettext

update:
	massificados
	pip install --upgrade pip & pip install -U -r requirements.txt

graph:
	rm -f massificados.png
	massificados & python manage.py graph_models -a -g -o  massificados.png



run:
	python manage.py runserver

migrate:
	massificados & manage.py migrate

install:
	./scripts/install.sh
	mkvirtualenv massificados & pip install -r requirements.txt
	make migrate

resetdb:
	dropdb -U massificados massificados
	createdb -U massificados --owner massificados --encoding "UTF-8" massificados
	rm -rf */migrations/000*
	rm -rf */migrations/001*
	massificados & python manage.py makemigrations
	massificados & python manage.py migrate
	massificados & python manage.py create_default
	massificados & python manage.py reset_pswd


mac_resetdb:
	dropdb massificados
	createdb --owner massificados --encoding "UTF-8" massificados
	rm -rf */migrations/000*
	rm -rf */migrations/001*
	massificados & python manage.py makemigrations
	massificados & python manage.py migrate
	massificados & python manage.py create_default
	massificados & python manage.py reset_pswd

update_deploy:
	rm -rf */migrations/000*
	rm -rf */migrations/001*
	python manage.py makemigrations
	git add -u
	git commit
	eb deploy

create_deploy:
	make resetdb
	git add -u
	git commit
	eb create -db -db.engine postgres