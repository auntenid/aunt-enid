#!/bin/bash
# Fix 502 Bad Gateway - Deployment script for Aunt Enid Campaign

set -e

PROJECT_DIR="/home/ubuntu/tr"
VENV_DIR="$PROJECT_DIR/.venv"

echo "=== Fixing 502 Bad Gateway ==="
echo ""

# 1. Navigate to project directory
cd "$PROJECT_DIR" || exit 1

# 2. Activate virtual environment
source "$VENV_DIR/bin/activate" || exit 1

# 3. Install/upgrade requirements
echo "Installing requirements..."
pip install -r requirements.txt --quiet

# 4. Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 5. Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# 6. Create log directories (in project directory - no sudo needed)
echo "Creating log directories..."
mkdir -p "$PROJECT_DIR/logs"

# 7. Stop any existing Gunicorn processes
echo "Stopping existing Gunicorn processes..."
sudo pkill -f gunicorn || true
sleep 2

# 8. Start Gunicorn manually (for testing)
echo "Starting Gunicorn..."
gunicorn --config gunicorn_config.py aunt_enid_campaign.wsgi:application --daemon

# 9. Wait a moment for Gunicorn to start
sleep 3

# 10. Check if Gunicorn is running
if pgrep -f gunicorn > /dev/null; then
    echo "✅ Gunicorn is running!"
    ps aux | grep gunicorn | grep -v grep
else
    echo "❌ Gunicorn failed to start. Check logs:"
    echo "   tail -f $PROJECT_DIR/logs/gunicorn_error.log"
    exit 1
fi

# 11. Test Gunicorn directly
echo ""
echo "Testing Gunicorn on localhost:8000..."
if curl -I http://127.0.0.1:8000 2>/dev/null | head -1; then
    echo "✅ Gunicorn is responding!"
else
    echo "❌ Gunicorn is not responding on port 8000"
    exit 1
fi

# 12. Setup nginx (if not already done)
echo ""
echo "Setting up nginx..."
if [ ! -f /etc/nginx/sites-available/aunt_enid ]; then
    sudo cp nginx_aunt_enid.conf /etc/nginx/sites-available/aunt_enid
    sudo ln -sf /etc/nginx/sites-available/aunt_enid /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default
    sudo nginx -t && sudo systemctl reload nginx
    echo "✅ Nginx configured!"
else
    echo "Nginx config already exists. Testing..."
    sudo nginx -t && sudo systemctl reload nginx
    echo "✅ Nginx reloaded!"
fi

# 13. Setup systemd service (optional, for auto-start)
echo ""
echo "Setting up systemd service..."
sudo cp aunt_enid_campaign_gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable aunt_enid_campaign_gunicorn.service
echo "✅ Systemd service configured (use 'sudo systemctl start aunt_enid_campaign_gunicorn' to use it)"

echo ""
echo "=== Deployment Complete ==="
echo ""
echo "Test your site:"
echo "  curl -I http://13.60.91.6"
echo ""
echo "If you still get 502, check:"
echo "  1. Gunicorn logs: tail -f $PROJECT_DIR/logs/gunicorn_error.log"
echo "  2. Nginx logs: sudo tail -f /var/log/nginx/error.log"
echo "  3. Gunicorn process: ps aux | grep gunicorn"
echo ""

