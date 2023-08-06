## Warning!!! Work in Progress! Not ready for production use at all yet.

# Django REST MediaBrowser

Client Loves CMS and Seperate JS Frontend. Thus born Django REST MediaBrowser. It will allow user to:

1. Upload Files and Images with ownership and share two-level mechanism(view and edit)
2. Keep your files safe unless you're the owner, or shared with you or the file is published publicly (Thanks to [django-private-storage](https://github.com/edoburu/django-private-storage)).
3. A beautiful REST-API (of course based on [django-rest-framewok](https://www.django-rest-framework.org)) to use the whole system and build a media manager frontend on top of it.

### Installation

Using pip:

```bash
pip install django-rest-filebrowser
```

Add this app and its dependencies in `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'taggit',
    'taggit_serializer',
    'private_storage',
    'django_filters',
    'rest_mediabrowser',
    #...
]
```

Add `rest_mediabrowser` urls in project's `urls.py`:

```python
urlpatterns = [
    #...
    path('mediabrowser/', include('rest_mediabrowser.urls')),
]
```

Migrate.

### TODO

1. Write tests.
2. Write a more comprehensive TODO.
3. Code vigorously for first stable release.
