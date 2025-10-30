import pytest
from app.models import Post
from django.db.models.signals import post_save

@pytest.mark.django_db
def test_post_save_signal_triggers():
    triggered = []

    def handler(sender, instance, created, **kwargs):
        triggered.append(True)

    post_save.connect(handler, sender=Post)
    Post.objects.create(title="Signal Test", content="ok")
    assert triggered
