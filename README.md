# SSO-Shell
SSH Extension software for Single Sign-on with SSH Certificates

# Documentation
[Click here for documentation](https://scheibling.github.io/sso-shell)

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
4. Install flask manually
```bash
$ pip install git+https://github.com/mitsuhiko/flask-oauth
```

5. Run the migrations
```bash
$ python manage.py migrate
```

6. Create a superuser
```bash
$ python manage.py createsuperuser
```

7. Create a certificate
```bash
$ python manage.py makecacert
```

7. Start the app
```bash
$ python manage.py runserver
```