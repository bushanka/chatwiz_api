import requests

headers = {
    'accept': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImJ1c2hhbmthIiwiZXhwIjoxNjk0NTA5NDQzfQ.ba-GqUh-iaeGmXqNAfX0n20T1bq2U-OMNFbzCNQJqqI',
}

response = requests.get('http://127.0.0.1:8000/users/', headers=headers)
print(response.text)