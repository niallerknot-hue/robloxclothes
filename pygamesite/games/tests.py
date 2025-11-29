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

    def test_game_list_view(self):
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Game")
        self.assertContains(response, "Test Dev")

    def test_game_detail_view(self):
        response = self.client.get(reverse('game_detail', args=[self.game.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Game")
        self.assertContains(response, "A test game description")

    def test_game_upload_view_get(self):
        response = self.client.get(reverse('game_upload'))
        self.assertEqual(response.status_code, 200)

    def test_game_upload_view_post(self):
        file_content = b"print('Hello World')"
        test_file = SimpleUploadedFile("game.py", file_content, content_type="text/x-python")

        data = {
            'title': 'New Game',
            'description': 'New Description',
            'developer': 'New Dev',
            'game_type': 'console',
            'game_file': test_file
        }

        response = self.client.post(reverse('game_upload'), data)
        self.assertEqual(response.status_code, 302) # Should redirect
        self.assertEqual(Game.objects.count(), 2)

        new_game = Game.objects.get(title='New Game')
        self.assertEqual(new_game.developer, 'New Dev')
