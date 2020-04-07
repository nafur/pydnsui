#!/bin/sh

cd /usr/local/apache2/htdocs/ && ./manage.py migrate

apachectl -D FOREGROUND