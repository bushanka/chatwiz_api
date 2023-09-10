import boto3

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

# Создать новый бакет
# s3.create_bucket(Bucket='linkup-test-bucket')

# Загрузить объекты в бакет

## Из строки
# s3.put_object(Bucket='linkup-test-bucket', Key='object_name', Body='TEST', StorageClass='COLD')

## Из файла

s3.upload_file('requirements_linux.txt', 'linkup-test-bucket', 'bushanka3228.txt')
# s3.upload_file('this_script.py', 'bucket-name', 'script/py_script.py')
