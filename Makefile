system_dependencies_dev:
    sudo apt-get install graphviz libgraphviz-dev graphviz-dev python-pygraphviz

system_dependencies:
    apt-get install gettext

update:
    ../env/bin/pip install --upgrade pip
    ../env/bin/pip install -U -r requirements.txt