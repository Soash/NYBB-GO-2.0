git clone https://github.com/Soash/NYBB-GO.git
cd .\NYBB-GO\

python -m venv venv
.\venv\Scripts\activate

pip install django==4.0.6 gunicorn whitenoise django-environ

cd .\project\

python manage.py runserver

