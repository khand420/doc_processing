# documents/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Document

class DocumentUploadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_upload_document(self):
        with open('path/to/test/image.png', 'rb') as file:
            response = self.client.post('/documents/upload/', {'file': file})
            self.assertEqual(response.status_code, 302)
            self.assertTrue(Document.objects.exists())
