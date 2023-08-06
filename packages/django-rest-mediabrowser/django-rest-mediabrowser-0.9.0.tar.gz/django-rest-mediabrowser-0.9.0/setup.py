import os
from pypandoc import convert_file
from setuptools import find_packages, setup

README = convert_file('README.md', 'rst')

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-rest-mediabrowser',
    version='0.9.0',
    packages=find_packages(),
    include_package_data=True,
    license='Mozilla Public License 2.0 (MPL 2.0)',
    description='A File Browser for REST API.',
    long_description=README,
    url='https://gitlab.com/codesigntheory/django-rest-mediabrowser',
    author='Utsob Roy',
    author_email='roy@codesign.com.bd',
    install_requires=[
        'djangorestframework',
        'pillow',
        'django-private-storage',
        'django-taggit',
        'django-taggit-serializer',
        'django-filter',
        'django-imagekit'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
