from django.db import models
from django.contrib.auth.models import User

LANG_CHOICES = [
    ("python", "Python"),
    ("cpp", "C++"),
    ("java", "Java"),
    ("javascript", "JavaScript")
]

# <i class="fa-brands fa-python"></i>
LANG_ICONS = {
    "python": "fa-python",
    "javascript": "fa-js",
    "java": "fa-java",
}


class Snippet(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANG_CHOICES)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now_add=True)
    views_count = models.PositiveIntegerField(default=0)
    public = models.BooleanField(default=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             blank=True, null=True)


class Comment(models.Model):
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    snippet = models.ForeignKey(to=Snippet, on_delete=models.CASCADE, related_name="comments")