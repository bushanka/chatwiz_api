import requests
import time

def login_sim():
    # ============= FIRST LOGIN - GET ACCESS AND REFRESH TOKEN =============
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'grant_type': '',
        'username': 'SparklingChatwiz',
        'password': 'BeY3ZcZDL$1Q3f8hGqHLq15@TQql7tXWof5wPmWS',
        'scope': '',
        'client_id': '',
        'client_secret': '',
    }

    response = requests.post('http://127.0.0.1:8000/token/', headers=headers, data=data)
    data =response.json()
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    print("loged in")
    print(access_token)
    return access_token, refresh_token


def request_from_user_with_access_token(access_token):
    # ============= CHECK ACCESS AND REFRESH TOKEN =============
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get('http://127.0.0.1:8000/users/', headers=headers)
    # access should work
    if response.status_code == 200:
        print('access token working - OK')
    else:
        raise Exception('access_token not working')


def request_from_user_with_refresh_token(refresh_token):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {refresh_token}',
    }
    response = requests.get('http://127.0.0.1:8000/users/', headers=headers)
    # refresh should not work
    if response.status_code != 200:
        print('refresh token NOT working - OK')
    else:
        raise Exception('refresh_token working')


def request_from_user_with_expired_access_token(access_token):
    # ============= CHECK ACCESS TOKEN EXPIRE =============
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get('http://127.0.0.1:8000/users/', headers=headers)
    if response.status_code != 200:
        print('access token expired - OK')
    else:
        raise Exception('access token not expired')


def exec_refresh_token(refresh_token):
    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    params = {
        'refresh_token': refresh_token,
    }

    response = requests.post('http://127.0.0.1:8000/token/refresh/', params=params, headers=headers)
    data =response.json()
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    print("Token refreshed")
    print(access_token)
    return access_token, refresh_token


if __name__ == '__main__':
    access_token, refresh_token = login_sim()
    request_from_user_with_access_token(access_token)
    request_from_user_with_refresh_token(refresh_token)
    time.sleep(70)
    request_from_user_with_expired_access_token(access_token)
    access_token, refresh_token = exec_refresh_token(refresh_token)
    request_from_user_with_access_token(access_token)
    request_from_user_with_refresh_token(refresh_token)
