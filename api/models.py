from django.db import models


# Create your models here.
class Message(models.Model):
    content = models.CharField(max_length=160, blank=False)
    views = models.PositiveIntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self) -> str:
        return f"Message {self.id}, views {self.views}," \
               f" content: {(self.content[:30] + '..') if len(self.content) > 30 else self.content}"
