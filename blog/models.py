from django.db import models

class Post(models.Model):
    """Simple blog post model for CRUD testing"""
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title