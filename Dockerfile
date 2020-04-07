FROM	httpd:latest
 
RUN	apt-get update && \
	apt-get install -y default-libmysqlclient-dev git python3-dev python3-pip && \
	pip3 install Django django-crispy-forms django-fontawesome-5 dnspython mod_wsgi mysqlclient && \
	echo "Include conf/extra/wsgi-express.conf" >> /usr/local/apache2/conf/httpd.conf && \
	echo "Include conf/extra/wsgi-django.conf" >> /usr/local/apache2/conf/httpd.conf && \
	mod_wsgi-express module-config >> /usr/local/apache2/conf/extra/wsgi-express.conf

COPY	.wsgi-django.conf /usr/local/apache2/conf/extra/wsgi-django.conf

EXPOSE	80

ADD	. /usr/local/apache2/htdocs/

RUN	cd /usr/local/apache2/htdocs/ && \
	./manage.py collectstatic && \
	./manage.py migrate

CMD	["apachectl", "-D", "FOREGROUND"]
