FROM nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

RUN mkdir /etc/nginx/keys/
COPY fullchain.pem /etc/nginx/keys/fullchain.pem
COPY privkey.pem /etc/nginx/keys/privkey.pem

# COPY lovelogo /etc/nginx/sites-available/www.lovelogo.ru

# RUN mkdir /etc/nginx/sites-enabled/
# RUN ln -s /etc/nginx/sites-available/www.lovelogo.ru /etc/nginx/sites-enabled/
