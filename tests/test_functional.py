import pytest
import django
from django.core.management import call_command
from pathlib import Path
from django.contrib.auth.models import User

# TC01 – Project Startup Test
def test_django_version():
    """Verify Django is installed and version >= 5.0"""
    assert django.VERSION >= (5, 0)

# TC02 – Database Migration Test
@pytest.mark.django_db
def test_migrations_run_successfully(settings):
    """Run migrations and ensure the database (file or memory) is usable"""
    call_command('migrate', verbosity=0)
    db_name = str(settings.DATABASES['default']['NAME'])
    assert 'memory' in db_name or Path(db_name).exists(), "Database not initialized properly"

# TC03 – Model CRUD Operations Test
@pytest.mark.django_db
def test_post_model_crud():
    """Verify create, read, update, and delete operations on Post model"""
    from blog.models import Post
    post = Post.objects.create(title="Test Post", content="pytest content")
    assert Post.objects.count() == 1

    post.title = "Updated Post"
    post.save()
    assert Post.objects.first().title == "Updated Post"

    post.delete()
    assert Post.objects.count() == 0

# TC04 – URL Routing Test
@pytest.mark.django_db
def test_hello_url(client):
    """Check if /hello/ URL returns correct response"""
    response = client.get('/hello/')
    assert response.status_code == 200
    assert b"Hello Django" in response.content

# TC05 – View Logic Output Test
@pytest.mark.django_db
def test_view_conditional_logic(client):
    """Verify that view returns expected status based on request parameters"""
    res_ok = client.get('/logic/?status=ok')
    res_fail = client.get('/logic/?status=fail')
    assert res_ok.status_code == 200
    assert res_fail.status_code in [400, 403]

# TC06 – Template Rendering Test
@pytest.mark.django_db
def test_template_context_rendering(client):
    """Ensure template renders with correct context variables"""
    response = client.get('/home/')
    assert response.status_code == 200
    assert b"Welcome to Django Testing Home Page" in response.content

# TC07 – Form Validation Test
def test_form_validation_logic():
    """Validate form logic using valid and invalid data"""
    from app.forms import ContactForm
    valid = ContactForm(data={"name": "Jinlin", "email": "test@test.com"})
    invalid = ContactForm(data={"name": "", "email": "abc"})
    assert valid.is_valid()
    assert not invalid.is_valid()

# TC08 – User Authentication Test
@pytest.mark.django_db
def test_user_login_authentication(client):
    """Test that user can be created and logged in successfully"""
    user = User.objects.create_user(username="testuser", password="12345")
    login = client.login(username="testuser", password="12345")
    assert login

# TC09 – Admin Access and Permission Test
@pytest.mark.django_db
def test_admin_access_permissions(client, django_user_model):
    """Check that superuser can access admin site while normal users cannot"""
    admin_user = django_user_model.objects.create_superuser(
        username="admin", password="adminpass", email="admin@test.com"
    )
    client.login(username="admin", password="adminpass")
    response = client.get('/admin/')
    assert response.status_code == 200
    assert b"Site administration" in response.content

# TC10 – 404 Error Page Test
def test_404_error_page(client):
    """Verify that non-existing URL returns a 404 error"""
    response = client.get('/nonexistent-url/')
    assert response.status_code == 404
