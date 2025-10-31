import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create_post_with_empty_title(client):
    """Try to create a post with an empty title — should fail gracefully."""
    # Send POST request with missing title
    response = client.post(reverse('create_post'), {'title': '', 'body': 'Some text'})
    # The server should return either 200 (with error message) or 400 (bad request)
    assert response.status_code in [200, 400]
    # Check that an error message or keyword appears in the response
    assert b'This field is required' in response.content or b'error' in response.content.lower()


@pytest.mark.django_db
def test_access_restricted_page_without_login(client):
    """Access a restricted page without authentication — should redirect to login."""
    response = client.get(reverse('dashboard'))
    # Unauthenticated users are typically redirected (HTTP 302)
    assert response.status_code == 302
    # Confirm that the redirect leads to the login page
    assert '/login' in response.url
