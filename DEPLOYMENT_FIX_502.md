# Fix 502 Bad Gateway - Quick Guide

## Problem
Nginx returns 502 Bad Gateway because Gunicorn (Django app server) is not running.

## Solution

### On your EC2 server, run these commands:

```bash
cd ~/tr

# 1. Make sure you're in the virtual environment
source .venv/bin/activate  # or: source env/bin/activate

# 2. Install/update requirements
pip install -r requirements.txt

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Run migrations
python manage.py migrate --noinput

# 5. Stop any existing Gunicorn
pkill -f gunicorn || true

# 6. Start Gunicorn (runs in background)
gunicorn --config gunicorn_config.py aunt_enid_campaign.wsgi:application --daemon

# 7. Wait a moment, then check if it's running
sleep 2
ps aux | grep gunicorn | grep -v grep

# 8. Test Gunicorn directly
curl -I http://127.0.0.1:8000

# 9. Configure nginx (if not already done)
sudo cp nginx_aunt_enid.conf /etc/nginx/sites-available/aunt_enid
sudo ln -sf /etc/nginx/sites-available/aunt_enid /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

# 10. Test your site
curl -I http://13.60.91.6
```

### Or use the automated script:

```bash
cd ~/tr
chmod +x deploy_fix_502.sh
./deploy_fix_502.sh
```

## Troubleshooting

### If Gunicorn won't start:
```bash
# Check logs
tail -f ~/tr/logs/gunicorn_error.log

# Try starting manually to see errors
gunicorn aunt_enid_campaign.wsgi:application --bind 127.0.0.1:8000
```

### If nginx still shows 502:
```bash
# Check nginx error log
sudo tail -f /var/log/nginx/error.log

# Verify Gunicorn is listening on port 8000
netstat -tlnp | grep 8000
# or
ss -tlnp | grep 8000

# Check nginx config
sudo nginx -t
```

### Common issues:
1. **Port 8000 already in use**: Change port in `gunicorn_config.py` or kill the process using it
2. **Permission errors**: Make sure `ubuntu` user owns the project directory
3. **Database errors**: Run `python manage.py migrate`
4. **Static files missing**: Run `python manage.py collectstatic`

## Auto-start on boot (optional)

To make Gunicorn start automatically:

```bash
sudo cp aunt_enid_campaign_gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable aunt_enid_campaign_gunicorn.service
sudo systemctl start aunt_enid_campaign_gunicorn.service
```

Check status:
```bash
sudo systemctl status aunt_enid_campaign_gunicorn.service
```

