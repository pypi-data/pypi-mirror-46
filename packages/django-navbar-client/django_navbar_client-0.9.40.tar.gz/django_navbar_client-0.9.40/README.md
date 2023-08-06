A Django App to integrate remote Navbar+Oauth  into local user models
## Install

In order to intall  simply use pip

```
pip install django_navbar_client
```

## Usage

Simply add django_navbar_client to your settings.py:

```python
INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
    ...
'django_navbar_client',
    ...
]

OAUTH_CLIENT_ID = "OAUTH_CLIENT_ID"
OAUTH_CLIENT_SECRET = "OAUTH_CLIENT_SECRET"
OAUTH_SERVER_URL = "OAUTH_SERVER_URL"

----

This library is partially funded  by the [Waste4Think proyect](http://waste4think.eu/) that  has received funding from the European Union’s [Horizon 2020](https://ec.europa.eu/programmes/horizon2020/) research and innovation program under grant agreement 688995.
The dissemination of results herein reflects only the author’s view and the European Commission is not responsible for any use that may be made of the information it contains.

