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


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"Tag: {self.name}"


class Snippet(models.Model):
    class Meta:
        ordering = ['name', 'lang']

    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANG_CHOICES)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, null=True)  # updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(default='', blank=True)  # Допустим, description может быть пустым
    views_count = models.PositiveIntegerField(default=0)
    public = models.BooleanField(default=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             blank=True, null=True)
    # many to many created additional table . Thats why we don't need default values
    tags = models.ManyToManyField(to='Tag')

    def __str__(self):
        return f"S: {self.name}|{self.lang} views:{self.views_count} public:{self.public} user:{self.user}"

    def __repr__(self):
        return f"S: {self.name}|{self.lang} views:{self.views_count} public:{self.public} user:{self.user}"


class Comment(models.Model):
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    snippet = models.ForeignKey(to=Snippet, on_delete=models.CASCADE, related_name="comments")

    def __repr__(self):
        return f"C: {self.text[:10]} author:{self.author} sn: {self.snippet.name}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('comment', 'Новый комментарий'),
        ('like', 'Новый лайк'),
        ('follow', 'Новый подписчик'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Уведомление для {self.recipient.username}: {self.title}"
