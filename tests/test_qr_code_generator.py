import requests

Endpoint='http://127.0.0.1:5000'

def test_can_call_endpoint():
    response= requests.get(Endpoint)
    assert response.status_code==200
    pass