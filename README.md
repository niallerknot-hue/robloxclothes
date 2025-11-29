# PyGameHub

A modern gaming site specifically for Python-based games.

## Features

- Browse a collection of Python games.
- Upload your own Python games (.py or .zip).
- Download games to play locally.
- Modern, dark-themed UI built with Tailwind CSS.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   cd pygamesite
   python manage.py migrate
   ```

3. Run the server:
   ```bash
   python manage.py runserver
   ```

4. Visit `http://127.0.0.1:8000` in your browser.

## Deployment

A `Dockerfile` is included for containerized deployment.
