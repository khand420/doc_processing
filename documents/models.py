# documents/models.py
from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

class ExtractedText(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    text = models.TextField()

class AIResult(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    entities = models.JSONField()  # Store entities as a JSON object
    classifications = models.CharField(max_length=255, null=True, blank=True)
    sentiment = models.CharField(max_length=50, null=True, blank=True)
