import requests

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImtpcmlsbF9rMWx2aW4iLCJleHAiOjE2OTQ1NDYwOTd9.8oAOdrwtzFgcqy4XM4Bs7cpTU4_4hwZpKuIE-BM_9oo',
}

response = requests.get('http://127.0.0.1:8000/users/', headers=headers)
print(response.text)