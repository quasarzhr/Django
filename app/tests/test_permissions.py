import pytest
from django.contrib.auth.models import User
from django.urls import reverse

@pytest.mark.django_db
def test_admin_access(client):
    admin = User.objects.create_superuser(username='admin', password='adminpass', email='a@a.com')
    client.login(username='admin', password='adminpass')
    response = client.get(reverse('admin:index'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_non_admin_redirect(client):
    user = User.objects.create_user(username='user', password='test123')
    client.login(username='user', password='test123')
    response = client.get(reverse('admin:index'))
    assert response.status_code == 302
