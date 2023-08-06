import pytest

from csirtgsdk.search import Search
from csirtgsdk.client.http import HTTP as Client

@pytest.fixture
def client():
    return Client()


def test_search(client):
    f = Search(client)

    assert f.client