FROM nginx

COPY lovelogo /etc/nginx/sites-available/www.lovelogo.ru
RUN mkdir /etc/nginx/sites-enabled/
RUN ln -s /etc/nginx/sites-available/www.lovelogo.ru /etc/nginx/sites-enabled/
