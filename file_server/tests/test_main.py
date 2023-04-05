import pytest
import mongomock
import io
from unittest.mock import patch
import requests
from file_server import main

@pytest.fixture()
def app():
    with patch.object(main, 'get_db_client', return_value=mongomock.MongoClient()):
        yield main.create_app()

@pytest.fixture()
def client(app):
    return app.test_client()

#Test function to test the upload_file function
def test_upload_file_1(client):
    file = "../test.jpg"
    data = {
        'file': (open(file, 'rb'), file),
        'tags' : "meow cat cute",
        'owner' : "111"
    }
    response = client.post('/images/upload', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 201
    assert response.json['file'] == file.split('/')[-1]

#Test function to test the upload_file function if tags are missing
def test_upload_file_2(client):
    file = "../test.jpg"
    data = {
        'file': (open(file, 'rb'), file),
        'owner' : "111"
    }
    response = client.post('/images/upload', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 400
    assert response.json['error'] == "Missing fields"

#Test function to test the upload_file function if owner is missing
def test_upload_file_3(client):
    file = "../test.jpg"
    data = {
        'file': (open(file, 'rb'), file),
        'tags' : "meow cat cute"
    }
    response = client.post('/images/upload', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 400
    assert response.json['error'] == "Missing fields"

#Test function to test get_image function
def test_get_image_1(client):
    response = client.get('/images/test.jpg')
    
    assert response.status_code == 200

#Test function to test get_image function if the image is missng
def test_get_image_2(client):
    response = client.get('/images/this_image_isnt_real.jpg')
    
    assert response.status_code == 404

#Test function to test get_image_by_id function
def test_get_image_byid_1(client):
    file = "../test.jpg"
    data = {'file': (open(file, 'rb'), file), 'tags' : "meow cat cute", 'owner' : "111"}
    client.post('/images/upload', data=data, content_type='multipart/form-data')
    response = client.get('/images/id/0')

    assert response.status_code == 200

#Test function to test get_image_by_id function if image is missing
def test_get_image_byid_2(client):
    response = client.get('/images/id/777')
    
    assert response.status_code == 404

# Testing get_user_images function
def test_get_user_images_1(client):
    file = "../test.jpg"
    data = [
        {'file': (open(file, 'rb'), file), 'tags' : "meow cat cute", 'owner' : "111"},
        {'file': (open(file, 'rb'), file), 'tags' : "dog meme funny", 'owner' : "111"},
        {'file': (open(file, 'rb'), file), 'tags' : "cat big funny", 'owner' : "222"},
        ]

    for each in data:
        response = client.post('/images/upload', data=each, content_type='multipart/form-data')

    response = client.get('/images/user/111')
    
    assert response.status_code == 200
    assert response.json['images'] == ['/images/test.jpg', '/images/test.jpg']

    response = client.get('/images/user/222')
    assert response.status_code == 200
    assert response.json['images'] == ['/images/test.jpg']

    response = client.get('/images/user/404')
    assert response.status_code == 404

# Testing get_images_by_tag function
def test_get_images_by_tag(client):
    file = "../test.jpg"
    data = [
        {'file': (open(file, 'rb'), file), 'tags' : "meow cat cute", 'owner' : "111"},
        {'file': (open(file, 'rb'), file), 'tags' : "dog meme funny", 'owner' : "111"},
        {'file': (open(file, 'rb'), file), 'tags' : "meow dog meme funny", 'owner' : "222"},
        ]

    for each in data:
        response = client.post('/images/upload', data=each, content_type='multipart/form-data')

    response = client.get('/images/tag/cat')
    assert response.status_code == 200
    assert len(response.json['images']) == 1

    response = client.get('/images/tag/meow')
    assert response.status_code == 200
    assert len(response.json['images']) == 2

    response = client.get('/images/tag/snake')
    assert response.status_code == 404

    