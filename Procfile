web: python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py populate_data && gunicorn aunt_enid_campaign.wsgi:application --bind 0.0.0.0:$PORT
