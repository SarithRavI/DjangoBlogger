import pytest
from django.test import TestCase,Client

client = Client()

@pytest.mark.django_db
def test_list_view():
    response = client.get('/blog/')
    assert response.status_code == 200 