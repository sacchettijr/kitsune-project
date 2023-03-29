cls
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata data.Usuarios.json
python manage.py loaddata data.Investimentos.json
python manage.py loaddata data.Retiradas.json
cls
python manage.py runserver