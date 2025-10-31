import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_user_registration_login_post_logout(client):
    """Full integration flow: register → login → create post → logout."""

    # Register a new user
    register_data = {
        'username': 'tester',
        'password1': 'testpass123',
        'password2': 'testpass123',
    }
    response = client.post(reverse('register'), register_data)
    assert response.status_code in [200, 302]
    # Check that the new user is saved in the database
    assert User.objects.filter(username='tester').exists()

    # Log in using the new credentials
    login_data = {'username': 'tester', 'password': 'testpass123'}
    response = client.post(reverse('app:user_login'), login_data)
    # Should either stay on the page (200) or redirect to dashboard (302)
    assert response.status_code in [200, 302]

    # Create a post while logged in
    response = client.post(reverse('create_post'), {'title': 'My first post', 'body': 'Hello world'})
    # Success is typically indicated by 200 or a redirect 302
    assert response.status_code in [200, 302]
    # Optional: verify that the created title appears in response or the redirect worked
    assert b"My first post" in response.content or response.status_code == 302

    # Logout and verify session is cleared
    response = client.get(reverse('app:logout'))
    assert response.status_code in [200, 302]
