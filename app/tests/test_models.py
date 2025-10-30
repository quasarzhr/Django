import pytest
from app.models import Post

@pytest.mark.django_db
def test_post_model_str():
    post = Post.objects.create(title="Test title", content="Some text")
    assert str(post) == "Test title"

@pytest.mark.django_db
def test_post_model_save_and_retrieve():
    post = Post.objects.create(title="Hello", content="World")
    saved_post = Post.objects.get(title="Hello")
    assert saved_post.content == "World"
