import os
import shutil
import zipfile
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from .models import Game
from django.core.files.uploadedfile import SimpleUploadedFile

class GameTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.game = Game.objects.create(
            title="Test Game",
            description="A test game description",
            developer="Test Dev",
            game_type="pygame"
        )
        # Prepare a dummy zip file for testing
        self.zip_path = os.path.join(settings.BASE_DIR, 'test_game.zip')
        with zipfile.ZipFile(self.zip_path, 'w') as zf:
            zf.writestr('index.html', '<h1>Game Running!</h1>')

    def tearDown(self):
        if os.path.exists(self.zip_path):
            os.remove(self.zip_path)
        # Clean up media directory after tests
        builds_dir = os.path.join(settings.MEDIA_ROOT, 'builds')
        if os.path.exists(builds_dir):
            shutil.rmtree(builds_dir)

    def test_game_list_view(self):
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Game")
        self.assertContains(response, "Test Dev")

    def test_game_detail_view(self):
        response = self.client.get(reverse('game_detail', args=[self.game.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Game")

    def test_game_upload_and_play(self):
        with open(self.zip_path, 'rb') as f:
            zip_file = SimpleUploadedFile("game.zip", f.read(), content_type="application/zip")

        data = {
            'title': 'Browser Game',
            'description': 'Playable in browser',
            'developer': 'Web Dev',
            'game_type': 'web',
            'browser_build': zip_file
        }

        response = self.client.post(reverse('game_upload'), data)
        self.assertEqual(response.status_code, 302)

        # Verify game created
        game = Game.objects.get(title='Browser Game')
        self.assertTrue(game.browser_build)

        # Verify extraction
        extract_path = os.path.join(settings.MEDIA_ROOT, 'builds', str(game.pk), 'index.html')
        self.assertTrue(os.path.exists(extract_path))

        # Verify Play URL
        play_url = reverse('play_game_index', args=[game.pk])
        response = self.client.get(play_url)
        self.assertEqual(response.status_code, 200)
        # FileResponse reads file in chunks/iterator, so we check headers or streaming content
        self.assertEqual(response['Content-Type'], 'text/html')
