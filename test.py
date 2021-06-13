import datetime
from unittest.mock import patch
import pytest
from main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_no_items(client):
    items = client.get("/items/")
    assert b'[]' == items.data


# @patch('datetime.date', return_value=datetime.date(1987, 6, 15))
def test_create_item(client):
    items = client.get("/items/create/", data={'file_name': 'hello_world', 'media_type': 'image'})
    assert b"Item created. {'id': 1, 'file_name': 'hello_world', 'media_type': 'image', 'created_at': datetime.datetime(2021, 6, 2, 13, 14, 46, 211570), 'updated_at': datetime.datetime(2021, 6, 2, 13, 14, 46, 211576)}" == items.data
