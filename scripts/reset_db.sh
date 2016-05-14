echo ''
echo 'Dropping Database'
echo ''

sudo rm -rf src/*/migrations/000*
env/bin/python src/manage.py makemigrations
dropdb massificados
createdb --encoding "UTF-8" massificados
env/bin/python src/manage.py migrate
env/bin/python src/manage.py create_default

echo 'Database was gracefully recreated... and cleared /ô'
echo ''