# CHATWIZ API

```
# Инструкции по установке и настройке проекта

## Шаг 1: Установка Certbot
```bash
sudo apt install --classic certbot
```

## Шаг 2: Получение SSL-сертификата
```bash
sudo certbot certonly --standalone
```

## Шаг 3: Установка Nginx
```bash
sudo apt-get install nginx
```

## Шаг 4: Настройка конфигурации Nginx

### 4.1: Переход в директорию sites-available
```bash
cd /etc/nginx/sites-available/
```

### 4.2: Создание файла конфигурации www.lovelogo.ru
```bash
sudo nano www.lovelogo.ru
```

#### Вставить следующий код в файл www.lovelogo.ru:
```nginx
server {
    listen 80;
    server_name www.lovelogo.ru;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name www.lovelogo.ru;

    ssl_certificate /home/bush/project/chatwiz/chatwiz_api/fullchain.pem;
    ssl_certificate_key /home/bush/project/chatwiz/chatwiz_api/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4.3: Создание символической ссылки для активации сайта
```bash
sudo ln -s /etc/nginx/sites-available/www.lovelogo.ru /etc/nginx/sites-enabled/
```

## Шаг 5: Проверка конфигурации Nginx
```bash
sudo nginx -t
```

## Шаг 6: Перезапуск службы Nginx
```bash
sudo service nginx restart
```

## Шаг 7: Запуск приложения

### 7.1: Откройте корневую директорию проекта и создайте два терминала

### 7.2: Активация виртуального окружения
```bash
source .venv/bin/activate
```

### 7.3: Запуск Gunicorn
```bash
gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app --bind 127.0.0.1:8000
```

### 7.4: Переход в директорию llm/tasks и запуск Celery
```bash
cd llm/tasks | celery -A chatwiztasks worker -Q chatwiztasks_queue --loglevel=INFO --hostname=chatwiz --autoscale=2,1
```

Теперь ваш проект должен быть успешно настроен и запущен. Откройте браузер и перейдите по адресу `https://www.lovelogo.ru`, чтобы убедиться, что он работает корректно.
```
