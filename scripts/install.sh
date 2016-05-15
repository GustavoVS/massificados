#!/bin/bash

echo ''
echo "Massificados: Ubuntu-trusty-based distributions install script"
echo ''
echo "Massificados: Installing System Dependencies."
echo ''

sudo apt-get install -y curl postgresql libpq-dev libjpeg-dev libpng12-dev build-essential python-dev gettext python-virtualenv


# Instalando referências para a última versão do node
echo 'Massificados: Installing Node e Ruby'
echo ''
curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
sudo apt-get install -y nodejs ruby
sudo update-alternatives --install /usr/bin/node node /usr/bin/nodejs 10
sudo npm install -g uglify-js uglifycss postcss-cli autoprefixer autoprefixer-cli
sudo gem install sass --no-ri --no-rdoc

echo 'Massificados: Installing Virtualenv'
echo ''

virtualenv env

echo 'Massificados: Installing App Dependencies'
echo ''

env/bin/pip install -r src/requirements.txt

echo 'Massificados: Configuring Database'
echo ''

sudo useradd --groups sudo --create-home massificados
sudo su - postgres -c "createuser -d massificados"
sudo -u postgres createdb --owner massificados --encoding "UTF-8" massificados

sudo -u massificados env/bin/python src/manage.py migrate
sudo -u massificados env/bin/python src/manage.py create_default

echo 'Massificados: Everything was Gracefully Installed /ô'
echo ''
