Команды:

.\venv\Scripts\activate.bat

django-admin startproject cinema
cd cinema
python manage.py startapp main
cd ..

pip install scikit-learn
pip install django
pip install numpy
pip install pandas

docker-compose up

cd cinema
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

python manage.py runserver
