from fastapi.testclient import TestClient
import pytest
import pathlib
import shutil
from pathlib import Path
import os
import sys
sys.path.append('../')
print(sys.path)
from api import app

client = TestClient(app)


def test_authorization():
    json_data = {
        "output_dest": "file",
        "output_file": "urltest_out.png"
    }
    # Define headers
    headers = {
        "access-token": "X9g218KJ9AwKG4KRPHbKUJzYK-FLBS8neybUEV6cO_w",
        "Content-Type": "application/json"
    }
    # Send the POST request with JSON data and headers
    response = client.post("/rheedconverter", json=json_data, headers=headers)
    assert response.status_code == 401
    assert response.json() == {
        "detail":"Unauthorized"
    }

def test_too_few_inputs(monkeypatch):
    def redefined_authorized(access_token, endpoint_id, params):
        return True
    monkeypatch.setattr("api.authorized", redefined_authorized)
    json_data = {
        "output_dest": "file",
        "output_file": "test_out.png"
    }
    # Define headers
    headers = {
        "access-token": "",
        "Content-Type": "application/json"
    }
    # Send the POST request with JSON data and headers
    response = client.post("/rheedconverter", json=json_data, headers=headers)
    assert response.status_code == 400
    assert response.json() == {
        "detail":"Incorrect number of parameters"
    }

def test_no_input_file(monkeypatch):
    def redefined_authorized(access_token, endpoint_id, params):
        return True
    monkeypatch.setattr("api.authorized", redefined_authorized)
    json_data = {
        "input_file": "data/rheed/test.img",
        "output_dest": "file"
    }
    # Define headers
    headers = {
        "access-token": "",
        "Content-Type": "application/json"
    }
    # Send the POST request with JSON data and headers
    response = client.post("/rheedconverter", json=json_data, headers=headers)
    assert response.status_code == 400
    assert response.json() == {
        "detail":"When the output destination is file, there must be a designated output file"
    }

def test_no_input_folder(monkeypatch):
    def redefined_authorized(access_token, endpoint_id, params):
        return True
    monkeypatch.setattr("api.authorized", redefined_authorized)
    json_data = {
        "input_file": "data/mbe/mbe_test_data",
        "output_dest": "folder"
    }
    # Define headers
    headers = {
        "access-token": "",
        "Content-Type": "application/json"
    }
    # Send the POST request with JSON data and headers
    response = client.post("/mbeparser", json=json_data, headers=headers)
    assert response.status_code == 400
    assert response.json() == {
        "detail":"While the output destination is a folder, there must be a designated output folder"
    }

def test_bad_file_input(monkeypatch):
    def redefined_authorized(access_token, endpoint_id, params):
        return True
    monkeypatch.setattr("api.authorized", redefined_authorized)
    json_data = {
        "input_file": "data/rheed/test1.img",
        "output_dest": "file"
    }
    # Define headers
    headers = {
        "access-token": "",
        "Content-Type": "application/json"
    }
    # Send the POST request with JSON data and headers
    response = client.post("/rheedconverter", json=json_data, headers=headers)
    assert response.status_code == 400
    assert "Error: Failed to validate path." in str(response.json()) 

def test_bad_output_type(monkeypatch):
    def redefined_authorized(access_token, endpoint_id, params):
        return True
    monkeypatch.setattr("api.authorized", redefined_authorized)
    json_data = {
        "input_file": "data/rheed/test.img",
        "output_dest": "file",
        "output_file": "test_out.png",
        "output_type": "none"
    }
    # Define headers
    headers = {
        "access-token": "",
        "Content-Type": "application/json"
    }
    # Send the POST request with JSON data and headers
    response = client.post("/mbeparser", json=json_data, headers=headers)
    print("Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response JSON:", response.json())  # Shows JSON data if the response is in JSON format
    print("Response Text:", response.text)
    assert response.status_code == 400
    assert response.json() == {
        "detail":"Incorrect output_type: output_type options are raw, JSON"
    } 

def test_bad_output_type(monkeypatch):
    def redefined_authorized(access_token, endpoint_id, params):
        return True
    monkeypatch.setattr("api.authorized", redefined_authorized)
    json_data = {
        "input_file": "data/rheed/test.img",
        "output_dest": "file",
        "output_file": "test_out.png",
        "output_type": "none"
    }
    # Define headers
    headers = {
        "access-token": "",
        "Content-Type": "application/json"
    }
    # Send the POST request with JSON data and headers
    response = client.post("/rheedconverter", json=json_data, headers=headers)
    assert response.status_code == 400
    assert response.json() == {
        "detail":"Incorrect output_type: output_type options are raw, JSON"
    } 

def test_bad_output_dest(monkeypatch):
    def redefined_authorized(access_token, endpoint_id, params):
        return True
    monkeypatch.setattr("api.authorized", redefined_authorized)
    json_data = {
        "input_file": "data/rheed/test.img",
        "output_dest": "folder",
        "output_file": "test_out.png",
    }
    # Define headers
    headers = {
        "access-token": "",
        "Content-Type": "application/json"
    }
    # Send the POST request with JSON data and headers
    response = client.post("/rheedconverter", json=json_data, headers=headers)
    assert response.status_code == 400
    assert response.json() == {
        "detail":"Incorrect output_dest: output_dest options are file, caller"
    } 

def test_error_in_function(monkeypatch):
    def redefined_authorized(access_token, endpoint_id, params):
        return True
    monkeypatch.setattr("api.authorized", redefined_authorized)
    json_data = {
        "input_file": "data/rheed/test.img",
        "output_dest": "file",
        "output_file": "test_out.txt",
    }
    # Define headers
    headers = {
        "access-token": "",
        "Content-Type": "application/json"
    }
    # Send the POST request with JSON data and headers
    response = client.post("/rheedconverter", json=json_data, headers=headers)
    print("Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response JSON:", response.json())  # Shows JSON data if the response is in JSON format
    print("Response Text:", response.text)
    assert response.status_code == 500
    assert response.json() == {
        "detail":'Failed to convert file: an error occurred running the function "rheedconverter"'
    }

def test_successful_function_call_file(monkeypatch):
    def redefined_authorized(access_token, endpoint_id, params):
        return True
    monkeypatch.setattr("api.authorized", redefined_authorized)
    json_data = {
        "input_file": "data/rheed/test.img",
        "output_dest": "file",
        "output_file": "data/rheed/test_out.png",
    }
    # Define headers
    headers = {
        "access-token": "",
        "Content-Type": "application/json"
    }
    # Send the POST request with JSON data and headers
    response = client.post("/rheedconverter", json=json_data, headers=headers)
    print("Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response JSON:", response.json())  # Shows JSON data if the response is in JSON format
    print("Response Text:", response.text)
    assert response.status_code == 200
    assert response.json() == {
        'message': 'Files processed successfully','status': 'ok'
    }
    os.unlink("data/rheed/test_out.png")

def test_successful_function_call_json(monkeypatch):
    def redefined_authorized(access_token, endpoint_id, params):
        return True
    monkeypatch.setattr("api.authorized", redefined_authorized)
    json_data = {
        "input_file": "data/rheed/test.img",
        "output_dest": "file",
        "output_file": "data/rheed/test_out.png",
        "output_type": "JSON"
    }
    # Define headers
    headers = {
        "access-token": "",
        "Content-Type": "application/json"
    }
    # Send the POST request with JSON data and headers
    response = client.post("/rheedconverter", json=json_data, headers=headers)
    print("Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response JSON:", response.json())  # Shows JSON data if the response is in JSON format
    print("Response Text:", response.text)
    assert response.status_code == 200
    assert response.json() == {
        'message': 'Files processed successfully','status': 'ok'
    }
    os.unlink("data/rheed/test_out.png")

def test_successful_function_call_raw(monkeypatch):
    def redefined_authorized(access_token, endpoint_id, params):
        return True
    monkeypatch.setattr("api.authorized", redefined_authorized)
    json_data = {
        "input_file": "data/rheed/test.img",
        "output_dest": "file",
        "output_file": "data/rheed/test_out.png",
        "output_type": "raw"
    }
    # Define headers
    headers = {
        "access-token": "",
        "Content-Type": "application/json"
    }
    # Send the POST request with JSON data and headers
    response = client.post("/rheedconverter", json=json_data, headers=headers)
    print("Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response JSON:", response.json())  # Shows JSON data if the response is in JSON format
    print("Response Text:", response.text)
    assert response.status_code == 200
    assert response.json() == {
        'message': 'Files processed successfully','status': 'ok'
    }
    os.unlink("data/rheed/test_out.png")
