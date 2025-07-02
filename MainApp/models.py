from django.db import models

LANG_CHOICES = (
    ("python", "Python"),
    ("java", "Java"),
    ("js", "JavaScript"),
    ("cpp", "C++"),
)

# <i class="fa-brands fa-python"></i>
LANG_ICONS = {
    "python": "fa-python",
    "java": "fa-java",
    # "cpp": "<UNK>",
    "js": "fa-js",
}

class Snippet(models.Model):
    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=10, choices=LANG_CHOICES)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(default='', blank=True)  # Допустим, description может быть пустым
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
