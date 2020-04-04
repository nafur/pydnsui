FROM	httpd:latest
 
RUN	apt-get update && \
	apt-get install -y libmysqlclient-dev python3-dev python3-pip && \
	pip3 install Django django-crispy-forms django-fontawesome-5 dnspython mod_wsgi mysqlclient && \
	echo "Include conf/extra/wsgi-express.conf" >> /usr/local/apache2/conf/httpd.conf && \
	echo "Include conf/extra/wsgi-django.conf" >> /usr/local/apache2/conf/httpd.conf && \
	mod_wsgi-express module-config >> /usr/local/apache2/conf/extra/wsgi-express.conf && \
	echo "WSGIScriptAlias / /usr/local/apache2/htdocs/pydnsui/wsgi.py \n\
WSGIPythonPath /usr/local/apache2/htdocs \n\
<Directory /usr/local/apache2/htdocs/pydnsui> \n\
<Files wsgi.py> \n\
Require all granted \n\
</Files> \n\
</Directory>" >> /usr/local/apache2/conf/extra/wsgi-django.conf

EXPOSE	80

ADD	. /usr/local/apache2/htdocs/
COPY	pydnsui/settings_local.py /usr/local/apache2/htdocs/pydnsui/

CMD	["apachectl", "-D", "FOREGROUND"]