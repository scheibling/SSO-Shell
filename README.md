# SSO-Shell
SSH Extension software for Single Sign-on with SSH Certificates


# Installation
1. Create a new virtual environment:
```bash
$ python3 -m venv .venv
```
2. Activate the virtual environment:
```bash
$ source .venv/bin/activate
```
3. Install the requirements:
```bash
$ pip install -r requirements.txt
```
4. Run the migrations
```bash
$ python manage.py migrate
```
5. Create a superuser
```bash
$ python manage.py createsuperuser
```
6. Start the app
```bash
$ python manage.py runserver
```