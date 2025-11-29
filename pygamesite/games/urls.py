from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('game/<int:pk>/', views.game_detail, name='game_detail'),
    path('upload/', views.game_upload, name='game_upload'),
    path('play/<int:pk>/', views.play_game, name='play_game_index'),
    path('play/<int:pk>/<path:path>', views.play_game, name='play_game_file'),
]
