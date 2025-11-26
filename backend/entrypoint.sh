#!/bin/sh

# Wait for the database to be ready
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready!"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create superuser
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@gmail.com', 'admin');
    print('Superuser created successfully!');
else:
    print('Superuser already exists.');
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the Django server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000