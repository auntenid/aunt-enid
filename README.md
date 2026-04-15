# Aunt Enid Campaign - Django Project

This repository has been consolidated into a clean, Django-only project.

## Quick start

1. Create virtualenv and install dependencies:
   
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Set environment variables (example):

   ```bash
   export DJANGO_SECRET_KEY="change-me"
   export DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1"
   # Optional: Postgres in prod
   # export DB_NAME=...
   # export DB_USER=...
   # export DB_PASSWORD=...
   # export DB_HOST=...
   # export DB_PORT=5432
   # Optional: S3 media storage
   # export AWS_STORAGE_BUCKET_NAME=...
   # export AWS_ACCESS_KEY_ID=...
   # export AWS_SECRET_ACCESS_KEY=...
   # export AWS_S3_REGION_NAME=eu-north-1
   ```

3. Run migrations and start server:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

4. Collect static for production:

   ```bash
   python manage.py collectstatic --noinput
   ```

## Structure

- `aunt_enid_campaign/`: Django project configuration and settings (with production overrides)
- `website/`: Main application (models, views, admin, URLs, forms)
- `templates/`, `static/`: Frontend templates and static files
- `requirements.txt`: Dependencies (WhiteNoise, optional S3 via django-storages)

See `aunt_enid_campaign/KEEPING_AND_REMOVALS.md` for a summary of what was kept/removed and why.
# tr
