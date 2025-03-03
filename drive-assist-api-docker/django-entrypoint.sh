#!/bin/bash

# Встановлюємо змінну середовища для Django (замініть "myproject" на назву вашого проєкту)
export DJANGO_SETTINGS_MODULE=driveassist.settings

# Перевіряємо наявність міграцій та застосовуємо їх
echo "Creating and applying migrations..."
python manage.py makemigrations
python manage.py migrate

# Запуск Django з Gunicorn
echo "Starting Django app..." && exec gunicorn myproject.wsgi:application --config /app/gunicorn_config.py

#TODO: adapted to postgres
# #!/bin/bash

# # Встановлюємо змінну середовища для Django (ім'я проєкту змініть за потреби)
# export DJANGO_SETTINGS_MODULE=myproject.settings

# # Затримка, щоб дочекатися запуску PostgreSQL
# sleep 10

# # Виконуємо міграції
# if [ -d "/app/migrations" ]; then
#   echo "Migration dir already exists"
# else
#   echo "Creating migrations directory"
#   mkdir -p /app/migrations
# fi

# # Перевіряємо, чи є незафіксовані міграції, і запускаємо міграції
# echo "Applying migrations" && python manage.py makemigrations
# echo "Migrating database" && python manage.py migrate

# # Запуск Django з Gunicorn
# echo "Starting Django app..." && exec gunicorn myproject.wsgi:application --config /app/gunicorn_config.py