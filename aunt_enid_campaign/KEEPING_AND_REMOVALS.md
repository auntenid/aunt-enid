### What was kept and why

- `aunt_enid_campaign/` (project): Core Django project configuration, URLs, WSGI/ASGI, and environment-specific settings.
- `website/` (app): All application logic (models, views, admin, urls, forms, management commands, migrations).
- `manage.py`: Standard Django management entrypoint.
- `templates/` and `static/`: Centralized templates and static assets used by the Django app.
- `requirements.txt`: Locked dependencies needed to run the Django project (now includes WhiteNoise and optional S3 support).

### What was removed and why

- Standalone HTML directories and `index.html` files (e.g. `clarification-on-.../index.html`, etc.): Superseded by Django templates and dynamic pages.
- Root images and duplicate static files (`*.jpg`, `*.png`, `script.js`, `styles.css`, `security.js`): Static assets are managed via Django `static/`.
- Non-Django artifacts (`article.php`, AWS CLI bundle, PowerShell scripts, deployment status docs): Not required for a clean Django-only codebase.

### How to add content now

- Use the Admin to create `NewsArticle` entries with slugs and featured images.
- Extend templates in `templates/website/` and add assets under `static/`.

### Environment configuration

- Set `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, optional S3 vars (`AWS_STORAGE_BUCKET_NAME`, etc.), and production DB vars (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`).


