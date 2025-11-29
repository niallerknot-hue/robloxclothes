from django.db import models

class Game(models.Model):
    GAME_TYPES = [
        ('pygame', 'Pygame'),
        ('console', 'Console Script'),
        ('web', 'Web/PyScript'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    developer = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    game_file = models.FileField(upload_to='games/', blank=True, null=True, help_text="Upload .py or .zip file")
    game_url = models.URLField(blank=True, null=True, help_text="Link to source code or playable version")
    game_type = models.CharField(max_length=20, choices=GAME_TYPES, default='other')

    def __str__(self):
        return self.title
