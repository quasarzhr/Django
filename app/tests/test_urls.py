from django.urls import reverse, resolve
from app.views import home

def test_home_url_resolves_to_home_view():
    url = reverse('home')
    assert resolve(url).func == home
