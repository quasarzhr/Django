import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_home_template_contains_text(client):
    response = client.get(reverse('home'))
    assert b"Welcome" in response.content
