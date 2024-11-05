from fastapi.testclient import TestClient
import pytest
import pathlib
import shutil
from pathlib import Path
import sys
sys.path.append('../')
print(sys.path)
from api import app

client = TestClient(app)

def authorized(access_token, endpoint_id, params):
    return True

def test_authorization_inputs():
    response = client.get("/rheedconverter", headers={"access-token": "", "Content-Type": "application/json"}, data={"input_url":"https://github.com/paradimdata/project_chameleon/raw/main/tests/data/rheed/test.img","output_dest": "file","output_file": "urltest_out.png"})
    assert response.status_code == 200
    assert response.json() == {
        "detail":"Unauthorized"
    }

def test_rheed_inputs():
    response = client.get("/rheedconverter", headers={"access-token": "X9g218KJ9AwKG4KRPHbKUJzYK-FLBS8neybUEV6cO_w", "Content-Type": "application/json"}, data={"output_dest": "file","output_file": "urltest_out.png"})
    assert response.status_code == 400
    assert response.json() == {
        "detail":"Incorrect number of parameters"
    }