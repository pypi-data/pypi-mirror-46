# Tutorial
In this tutorial, I aim to introduce you to the most basic usage of *django-secret-settings*, a python package
facilitating to include secrets like, e.g., passwords or the Django `SECRET_KEY`, in a convenient and secure manner into
your Django settings. The mechanism to do so further provides, as a by-product, a means to switch between dedicated
settings for different environments (e.g., development, testing, staging, production, education, ...) as simple as only
conceivable.

In order to demonstrate both features, we will first build a minimalistic (and somewhat harebrained) Django project
displaying several quantities defined in the Django settings module, and then iteratively port this project
1. to use a settings package containing dedicated settings modules for each environment, and
2. to use django-secret-settings for secret management and settings switching.

Users familiar with Django may find the content of the beginning of this tutorial (in particular, the section [Getting
started with Django](#getting-started-with-django)) rather tedious. You are very welcome to skim through this chapter or
directly jump to [Using django-secret-settings](#using-django-secret-settings).

## Getting started with Django
### Building an example project to play with
We will start a brand new Django example project to begin with. On a linux machine having an installed Python 3.5, this
would be done somewhat like that (or course, adapt as necessary, e.g. a different Python version):
```bash
mkdir /home/$USER/tutorial-django-secret-settings
cd /home/$USER/tutorial-django-secret-settings
python3.5 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install Django
django-admin startproject mysite
```
This very basic template project only displays a debug page if we would navigate to it using a browser. Thus, we first
need to configure a URL mapping for the index page by changing `mysite/mysite/urls.py` to contain the following:
```python
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
]
```
The view `views.index` does, however, not exist yet. To account for that, create the file `mysite/mysite/views.py` with
the following content:
```python
from django.conf import settings
from django.http import HttpResponse


def index(request):
    return HttpResponse(
        '<h1>Hello World!</h1>'
        '<p>BASE_DIR = "{}"</p>'
        '<p>SECRET_KEY = "{}"</p>'.format(
            settings.BASE_DIR,
            settings.SECRET_KEY
        )
    )
```
In 'real life', you would `render` a template instead of using a `HttpResponse`, but in the context of this tutorial,
this seems perfectly fine. Importing `settings` from `django.conf` yields access to all the settings values defined in
`mysite/mysite/settings.py`, as these values are automatically resolved by Django on startup.

First milestone reached! If you now use the very same console from the beginning (in particular, the activated venv and
the current working directory are important) to run
```bash
python mysite/manage.py runserver
```
(ignore error messages regarding 'unapplied migration(s)'), and then visit http://localhost:8000 using your favorite
browser, you will see something like this:

    Hello World!

    BASE_DIR = "/home/cmahr/tutorial-django-secret-settings/mysite"
    SECRET_KEY = "My h0v3rcraft is fu11 of eels."

Of course, you will see your user name instead of 'cmahr', and it would be an extreme coincidence if Django had created
the very same `SECRET_KEY` as above ;-)

### Refactor Django project to use settings package
While a simple skeleton settings module created by Django is nice to start a new project, it will likely not suffice in
the long run. Oftentimes you end up having lots of different things configured in one huge file that you want to split
in multiple modules. This can be achieved by refactoring your settings module to a settings package as follows:

Create the file `mysite/mysite/settings/__init__.py`, in which you import all appropriate settings modules:
```python
from .settings import *
```
For simplicity, we have only import the already present `settings.py`, but you could add additional import statements
here. For the `.settings` module to be found, move it from `mysite/mysite/settings.py` to
`mysite/mysite/settings/settings.py`.
 
Voilà, you now have a settings package, with just one major problem: Your `BASE_DIR` has changed
* from `/home/$USER/tutorial-django-secret-settings/mysite`
* to `/home/$USER/tutorial-django-secret-settings/mysite/mysite`

(go on, verify by firing up the server again and check with your browser). This is deemed to confuse any app relying on
an appropriate value for this quantity, and to fix this issue, change it's definition in
`mysite/mysite/settings/settings.py` as follows:
```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### Different settings for different environments
It is rather common to have some 'base' settings that are the same for every environment (the `settings.TEMPLATES`
configuration oftentimes is such a base setting), as well as complementary settings that may very much depend on the
specific environment (e.g, `settings.SECRET_KEY`, `settings.DEBUG`, `settings.ALLOWED_HOSTS` or `settings.DATABASE`
configurations, to name just a few). A widespread solution is to use a directory structure as follows:

    mysite/mysite/settings/
    ├── base.py
    ├── development.py
    ├── __init__.py
    └── production.py
    
where `base.py` contains the base settings, `development.py` and `production.py` the environement-specific
settings, and the dunter init is used to include the 'correct' settings, e.g.
```python
from .development import *
```
Let's adapt to this settings structure! In our case, the `development.py` would contain
```python
from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'My h0v3rcraft is fu11 of eels.'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
and the `base.py` everything that was in `settings.py` except, of course, the values defined in `development.py`. The
new 'production' settings (of course, designed to work on our development machine) should look like this:
```python
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l#!6p7)-4xhy25@pu5$y$%k&7#8a(#1^89=^m*=e69xl**&!11'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_prod.sqlite3'),
    }
}


# Email
EMAIL_HOST = 'mail.localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'admin@localhost'
EMAIL_HOST_PASSWORD = 'a_very_secure_password'
EMAIL_USE_TLS = True
```
(We have introduced additional email settings, which will be useful later in the exercises.)

It is now pretty easy to switch settings based on the environment:
* simply change the import statement in `mysite/mysite/settings/__init__.py`
* reload the web server
* (check using your browser that everything went well)
 
Still, you remain with any secret values like, e.g., the Django `SECRET_KEY` or database passwords, in plain text. That's bad, and that's
where django-secret-settings comes in.

## Using django-secret-settings
### Bootstrapping Django settings using django-secret-settings
Given a Django project with a settings package as above, it's very simple to make use of django-secret-settings to load
the appropriate settings module for you: First, install django-secret-settings using pip
```bash
pip install django-secret-settings
```
and change the content of `mysite/mysite/settings/__init__.py` as follows:
```python
from django_secret_settings.autoload import *
```
Running `python mysite/manage.py runserver` will, however, fail:

    django_secret_settings.store.error.SecretStoreFactoryError: Did not find the store directory "secrets" in the settings directory "/home/cmahr/tutorial-django-secret-settings/mysite/mysite/settings"!
        This means that you do not have any secret stores available.
        If this is correct, please create the store directory by running
        $ mkdir "/home/cmahr/tutorial-django-secret-settings/mysite/mysite/settings/secrets"

Well, django_secret_settings is not wrong, we do not (yet) have any secret stores available. We will discuss shortly why
this is considered a fatal error. For now, just use the proposed `mkdir` command and try again (to find yet another
issue):

    django_secret_settings.store.error.SecretStoreFactoryError: Did not find exactly 1 private key in "/home/cmahr/tutorial-django-secret-settings/mysite/mysite/settings/secrets"!
        If you intend to use the development mode, please create a fake private key by running
        $ touch "/home/cmahr/tutorial-django-secret-settings/mysite/mysite/settings/secrets/development.pem"

I can downright hear you groan. Sorry about that. Please, give in another time, touch the `development.pem` file and try
again:

    The store_base_dir="/home/cmahr/tutorial-django-secret-settings/mysite/mysite/settings/secrets/development" is not a directory! This means that you do not have any secrets encrypted with the private_key_file="/home/cmahr/tutorial-django-secret-settings/mysite/mysite/settings/secrets/development.pem".
    The store_base_dir="/home/cmahr/tutorial-django-secret-settings/mysite/mysite/settings/secrets/development" is not a directory! This means that you do not have any secrets encrypted with the private_key_file="/home/cmahr/tutorial-django-secret-settings/mysite/mysite/settings/secrets/development.pem".
    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).

    You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
    Run 'python manage.py migrate' to apply them.

    May 12, 2019 - 16:22:00
    Django version 2.2.1, using settings 'mysite.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

This time, the server is coming up, the `BASE_DIR` is correct, and the `SECRET_KEY` as defined in `development.py`
is displayed (go on, verify that it's the value from the development settings module by changing it).
Django-secret-settings still 'complains' that the `mysite/mysite/settings/secrets/development` directory is not present,
and explains what this means: No secrets encrypted with the private key `development.pem` are present. Given, that this
file is a fake private key (it is empty, after all) this is perfectly normal and should not suprise you.

So, what's happening in the background is actually pretty simple, and you might have already guessed: When you
`import *` in the dunder init of your settings package, django-secret-settings first determines that your Django
settings package is `mysite.settings`, and that it is located at
`/home/$USER/tutorial-django-secret-settings/mysite/mysite/settings`.

Instead of making you configure in Python code which settings module (`development.py`, `production.py`) to load,
django-secret-settings looks for 'private key files' (*.pem) in `mysite/mysite/settings/secrets` and fails with a
`SecretStoreFactoryError` if this directory is not present and does not contain exactly 1 such private key file (as you
saw above). This is because the name of this file determines which settings module is subsequently imported. In
particular, if you rename `development.pem` to `production.pem`, then the production settings module will be loaded, as
you could tell from the different secret key being shown (if you try this, don't forget to undo this renaming
afterwards to still be able to follow this tutorial).

Please note that it was __not__ assumed that either a missing `secrets` directory or a missing private key file mean
'development mode': In the possible event that you fail to provision a suitable private key file in production, you do
not want to end up running with development settings!

### Handling *secret* settings
Despite the name being 'django-secret-settings', so far we have not talked about keeping secrets private. Let's change
that right here, right now! If you take a look at the 'production' settings from above, at least the `SECRET_KEY` and
the `EMAIL_HOST_PASSWORD` are not meant to be widely known. Further, the `EMAIL_HOST_USER` would be considered private
by some people.

Django-secret-setting uses standard [public-key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography), in
particular the [RSA algorithm](https://en.wikipedia.org/wiki/RSA_(algorithm)), acting on
[JSON](https://en.wikipedia.org/wiki/JSON) files in a suitable directory structure. This is due to the following
reasons:

* RSA is a secure, proven and available algorithm (at least until the quantum computing age).
* The private key file name is a suitable mechanism for selecting which settings module to import.
* The encrypted secrets may reside in the repository (or a separate submodule), thereby giving any developer the bird's
  eye view of the available secrets.
* The JSON format is simple and convenient for (de)serialization and allows the storage of 'complex' secrets.
* The public key is not secret and may hence reside in the repository besides the secrets. This way, any developer may
  conveniently add new secret files. (Adding additional information to existing secrets would be possible in principle.
  This feature is in the backlog, though yet to be implemented.)

Given this background, the first step is to create a new RSA public/private key pair for the production secrets:
```bash
openssl genrsa 4096 > mysite/mysite/settings/secrets/production.pem
```
This is your *private* key, and it is all that is necessary to decrypt any secrets in your production store. Therefore,
make __very sure__ to keep this file away from 'nosy people'. In particular, it does not belong in version control, so best
add, e.g., a .gitignore file in `mysite/mysite/settings/secrets/.gitignore`
```
/*.pem
```
Next, create a new directory to store your production secrets in
```bash
mkdir mysite/mysite/settings/secrets/production
```
and for convenience (see above; this step is not strictly necessary) we extract the public key and put it in the store
for simple creation of additional secrets:
```bash
openssl rsa -in mysite/mysite/settings/secrets/production.pem -pubout -out mysite/mysite/settings/secrets/production/public-key.pem
```

We are now prepared to add new secrets, and we start with the `SECRET_KEY`. Add `mysite/mysite/settings/secrets/production/django.json`
with this content:
```json
{
  "SECRET_KEY": "l#!6p7)-4xhy25@pu5$y$%k&7#8a(#1^89=^m*=e69xl**&!11"
}
```
Then, encrypt it with your production public key:
```bash
cd mysite/mysite/settings/secrets/production/
openssl rsautl -encrypt -pubin -inkey public-key.pem -in django.json -out django
```
You may take your favorite editor to take a look at the `django` file, but it's binary garbage. To verify, that the
encryption process went well, decrypt with the private key and compare:
```bash
openssl rsautl -decrypt -inkey ../production.pem -in django -out django.decrypted
diff django.json django.decrypted
```
There should be no visible output to the `diff` command. Finally, remove the unencrypted files by
```bash
rm django.json django.decrypted
```
and make sure that your editor has not created any or destroyed all temporary files that might contain sensitive data.

That's all, folks! You may now use your brand new encrypted secret in your 'production' settings file
`mysite/mysite/settings/production.py` as follows:
```python
from django_secret_settings.autoload import secret_store

SECRET_KEY = secret_store.get('django', 'SECRET_KEY')
```
If you now try to run `python mysite/manage.py runserver`, you will, however, once more face a
`SecretStoreFactoryError`:

    django_secret_settings.store.error.SecretStoreFactoryError: Found multiple private key files in the store search directory "/home/cmahr/tutorial-django-secret-settings/mysite/mysite/settings/secrets"!
        Please remove all private key files in this directory except the one you intend to use.
        Ambiguity is considered a fatal error for security reasons.

While in your first try, django-secret-settings did not find *any* private key file, it now found *two* (i.e.,
`development.pem` and `production.pem`). Again, instead of guessing and hence possibly ending up with something
dangerous, django-secret-settings refuses to work at all. Delete the empty development key file and verify that now
everything is working as expected!

### Exercise 1: Migrate email settings
You should now know everything necessary to also secure the email settings above. A possible solution would look like
this:

* Encrypt `mysite/mysite/settings/secrets/production/email.json`
  ```json
  {
    "HOST": {
      "USER": "admin@localhost",
      "PASSWORD": "admin"
    }
  }
  ```
  using `openssl` (see above). Don't forget to delete the plain text file afterwards! Caught any temporary files created
  by your editor?
* Use the `secret_store` in your production settings to obtain the newly created secrets:
  ```python
  EMAIL_HOST_USER = secret_store.get('email', 'HOST', 'USER')
  EMAIL_HOST_PASSWORD = secret_store.get('email', 'HOST', 'PASSWORD')
  ```
  Every call to `secret_store.get` is encrypting the secret file once, i.e., there is no caching mechanism implemented.
  If this is undesirable (or you just prefer this), you could also use
  ```python
  email_host_dict = secret_store.get('email', 'HOST')
  EMAIL_HOST_USER = email_host_dict['USER']
  EMAIL_HOST_PASSWORD = email_host_dict['PASSWORD']
  ```
  or even
  ```python
  email_dict = secret_store.get('email')
  EMAIL_HOST_USER = email_dict['HOST']['USER']
  EMAIL_HOST_PASSWORD = email_dict['HOST']['PASSWORD']
  ```

### Excercise 2: Add new encrypted settings for a staging environment
A possible solution might look like this:

* Create 'staging' settings `mysite/mysite/settings/staging.py`
  ```python
  from .base import *
  from django_secret_settings.autoload import secret_store
  
  # SECURITY WARNING: keep the secret key used in production secret!
  SECRET_KEY = secret_store.get('django', 'SECRET_KEY')
  
  # SECURITY WARNING: don't run with debug turned on in production!
  DEBUG = False
  
  ALLOWED_HOSTS = [
      'localhost',
      '127.0.0.1',
  ]
  
  # Database
  # https://docs.djangoproject.com/en/2.2/ref/settings/#databases
  
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': os.path.join(BASE_DIR, 'db_stag.sqlite3'),
      }
  }
  ```
* Create the 'staging' secret store
  ```bash
  mkdir mysite/mysite/settings/secrets/staging
  openssl genrsa 4096 > mysite/mysite/settings/secrets/staging.pem
  openssl rsa -in mysite/mysite/settings/secrets/staging.pem -pubout -out mysite/mysite/settings/secrets/staging/public-key.pem
  ```
* Encrypt `mysite/mysite/settings/secrets/staging/django.json`
  ```json
  {
    "SECRET_KEY": "@n(&o2b#iki^spc-o4)cy7w)xus2+aicto*2nbxe)%gff*0-c^"
  }
  ```
  using `openssl` (see above). Don't forget to delete the plain text file afterwards! Caught any temporary files created
  by your editor?
* Can't run because of multiple keys? Move your production private key to a secure place and try again.

## Conclusion
* django-secret-settings makes having securely encrypted secrets in our Django settings quite easy.
* You can have as many different environments as you like. Just have a dedicated store and private key file for each.
* Switching environments is done by switching the private key file (name).
* Granted, as of now, the manual usage of `openssl` is inconvenient. There will be Django management commands in future
  versions of this package.
