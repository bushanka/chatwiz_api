# CHATWIZ BACKEND

# Инструкции по установке и настройке проекта

## Шаг 1: Установка проекта
```bash
git clone https://github.com/bushanka/chatwiz_api.git
```
```bash
cd chatwiz_api
```

## Шаг 2: Установка Docker
```bash
sudo apt update
```
```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
```bash
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```
```bash
sudo apt install docker-ce
```
```bash
sudo usermod -aG docker ${USER}
```
Далее необходимо перезагрузить сервер, чтобы добавить docker в группу sudo

## Шаг 3: Установка certbot для создания ssl сертификатов
```bash
sudo apt install certbot
```

## Шаг 4: Создание сертификатов
Нужно чтобы порт 80 был свободен и для доменного имени была указана `А` ресурсная запись, которая указывает на IP машины 
```bash
sudo certbot certonly --standalone
```
Заполняем все поля. Указываем e-mail и доменное имя, например api.chatwiz.ru

## Шаг 5: Копируем сертификаты в папку nginx
```bash
sudo cat /etc/letsencrypt/live/your.domain.name/fullchain.pem > nginx/fullchain.pem
```
```bash
sudo cat /etc/letsencrypt/live/your.domain.name/privkey.pem > nginx/privkey.pem
```

## Шаг 6: Собираем докер-образы
Название для образа nginx - `chatwiz_nginx`. Для fastapi - `chatwiz_api`
```bash
cd nginx
```
```bash
docker build -t "chatwiz_nginx:latest"
```
```bash
cd ..
```
```bash
docker build -t "chatwiz_api:latest"
```

## Шаг 7: Запуск бека
```bash
docker compose up -d
```