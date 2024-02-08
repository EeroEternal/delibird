import requests


def test_ping():
    """Test ping."""
    host = "localhost"
    port = 8000
    url = f"http://{host}:{port}/ping"
    response = requests.get(url)
    print(f"response: {response.text}")
