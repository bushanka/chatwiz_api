import requests

headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',
}

response = requests.post('http://158.160.100.102:5000/billing/0/3', headers=headers)

print()