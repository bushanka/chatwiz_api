from yookassa import Payment, Configuration


Configuration.account_id = '252962'
Configuration.secret_key = 'test_88ebn3FSZvhXNwCbOkaHJmYQX1arNGx2H0QzU2Yxqn8'

payment_id = '2c8ea686-000f-5000-9000-14c437e81122'
payment = Payment.find_one(payment_id)
print(payment)