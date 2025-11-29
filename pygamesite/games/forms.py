from django import forms
from .models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'description', 'developer', 'cover_image', 'game_file', 'browser_build', 'game_url', 'game_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2'}),
            'developer': forms.TextInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2'}),
            'game_type': forms.Select(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2'}),
            'game_url': forms.URLInput(attrs={'class': 'w-full bg-gray-700 text-white rounded p-2'}),
        }
