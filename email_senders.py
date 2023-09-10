import smtplib

# Настройки почты отправителя
sender_email = "eclectronochki@mail.ru"
# sender_password = "kirillsasha2928"
sender_smtp_server = "smtp.mail.ru"
sender_smtp_port = 587

sender_email = "test"
external_password = 'nDrCe3dnATN683ABKxPn'
sender_password = external_password

# Настройки почты получателя
receiver_email = "k_vasyurin@mail.ru"

# Создаем сообщение
message = "Subject: Hello World\n\nHello World!"

# Отправляем сообщение
with smtplib.SMTP(sender_smtp_server, sender_smtp_port) as smtp_server:
    smtp_server.starttls()
    smtp_server.login(user=sender_email,
                      password=sender_password)
    smtp_server.sendmail(sender_email, receiver_email, message)
