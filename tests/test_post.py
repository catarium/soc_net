import pytest
import requests
import time


def test_post():
    url = 'http://127.0.0.1:8000'
    user1_name = time.time()
    user2_name = time.time() + 1

    session = requests.Session()

    # registration account 1
    body = {
        'name': str(user1_name),
        'password': 'test'
    }
    res = session.post(f'{url}/auth/registration', json=body)
    assert res.status_code == 200
    user1_id = res.json()['res']['id']

    # creating a post
    body = {
        'name': 'test',
        'text': 'test_text',
    }
    res = session.post(f'{url}/userapi/post', json=body)
    post_id = res.json()['res']['id']
    assert res.status_code == 200

    # getting a post
    res = session.get(f'{url}/userapi/post/{post_id}')
    assert res.status_code == 200

    # searching for a post
    res = session.get(f'{url}/userapi/post?user_id={user1_id}')
    assert res.status_code == 200

    # registration account 2
    body = {
        'name': str(user2_name),
        'password': 'test'
    }
    res = session.post(f'{url}/auth/registration', json=body)
    assert res.status_code == 200

    # updating not own post
    body = {
        'id': post_id,
        'name': 'update',
        'text': 'text'
    }
    res = session.put(f'{url}/userapi/post', json=body)
    assert res.status_code == 403

    # deleting not own post
    res = session.delete(f'{url}/userapi/post/{post_id}')
    assert res.status_code == 403

    # logging back to account 1
    body = {
        'name': str(user1_name),
        'password': 'test'
    }
    res = session.post(f'{url}/auth/login', json=body)
    print(res.json())

    # updating own post
    body = {
        'id': post_id,
        'name': 'update',
        'text': 'text'
    }
    res = session.put(f'{url}/userapi/post', json=body)
    assert res.status_code == 200

    # deleting own post
    res = session.delete(f'{url}/userapi/post/{post_id}')
    assert res.status_code == 200


