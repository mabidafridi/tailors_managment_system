import sys
import os

# Add project root to Python path so CI can find app.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


def test_home_page():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

