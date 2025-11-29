import os
import zipfile
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, FileResponse
import mimetypes
from .models import Game
from .forms import GameForm

def game_list(request):
    games = Game.objects.all().order_by('-created_at')
    return render(request, 'games/game_list.html', {'games': games})

def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'games/game_detail.html', {'game': game})

def game_upload(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save()
            if game.browser_build:
                # Extract the zip file
                zip_path = game.browser_build.path
                extract_path = os.path.join(settings.MEDIA_ROOT, 'builds', str(game.pk))
                os.makedirs(extract_path, exist_ok=True)

                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        for member in zip_ref.namelist():
                            # Security: Prevent Zip Slip (path traversal)
                            filename = os.path.basename(member)
                            if not filename:
                                continue

                            # Skip if absolute path or contains ..
                            src = member
                            dst = os.path.join(extract_path, src)

                            # Real path check
                            if not os.path.abspath(dst).startswith(os.path.abspath(extract_path)):
                                continue

                            zip_ref.extract(member, extract_path)
                except zipfile.BadZipFile:
                    # Handle error gracefully - for now just pass
                    pass

            return redirect('game_list')
    else:
        form = GameForm()
    return render(request, 'games/game_upload.html', {'form': form})

def play_game(request, pk, path='index.html'):
    """
    Serves the game files from the extracted build directory.
    """
    game = get_object_or_404(Game, pk=pk)
    file_path = os.path.join(settings.MEDIA_ROOT, 'builds', str(game.pk), path)

    # Security check: Ensure the path is within the game's build directory
    build_dir = os.path.abspath(os.path.join(settings.MEDIA_ROOT, 'builds', str(game.pk)))
    requested_path = os.path.abspath(file_path)

    if not requested_path.startswith(build_dir):
        raise Http404("Invalid file path")

    if os.path.exists(file_path) and os.path.isfile(file_path):
        # Determine content type
        content_type, encoding = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = 'application/octet-stream'

        # Specific overrides for web games
        if path.endswith('.wasm'):
            content_type = 'application/wasm'

        return FileResponse(open(file_path, 'rb'), content_type=content_type)
    else:
        # If index.html is requested but not found, try finding it in a subfolder?
        # For now, just 404
        raise Http404("File not found")
