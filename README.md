# PyGameHub

A modern gaming site specifically for Python-based games.

## Features

- **Game Browser:** Browse a collection of Python games with a modern, dark-themed UI.
- **Upload:** Developers can upload games as downloadable files (`.py` or `.zip`) or source URLs.
- **Browser Play:** Support for playing games directly in the browser! Upload a `.zip` build (containing `index.html` and assets), and it will be playable instantly on the site.
- **Download:** Users can download source files to play locally.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   cd pygamesite
   python manage.py migrate
   ```

3. **Run the server:**
   ```bash
   python manage.py runserver
   ```

4. **Visit** `http://127.0.0.1:8000` in your browser.

## How to Upload a Browser Game

To make your game playable in the browser:
1. Build your Python game for the web (e.g., using tools like **Pygbag** for Pygame).
2. Zip the output directory (ensure `index.html` is at the root of the zip archive).
3. On the Upload page, select your `.zip` file in the **"Browser Build (.zip)"** field.
4. Select "Web/PyScript" as the Game Type.
5. Submit! The game will appear with a "Play Now" window.

## Deployment

A `Dockerfile` is included for containerized deployment.

1. **Build the image:**
   ```bash
   docker build -t pygamesite .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 pygamesite
   ```
