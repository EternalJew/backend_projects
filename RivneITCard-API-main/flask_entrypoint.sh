#!/bin/bash
export FLASK_APP=run.py
# wait for postgres to start
sleep 10

if [ -d "/app/migrations/versions" ]; then
  echo "Migration dir already exists"
  echo "merge head" && flask db merge heads
else
  echo "init db" && flask db init
  cp -f /app/script.py.mako /app/migrations/script.py.mako
  echo "making migrations" && flask db migrate
fi

echo "updating db" && flask db upgrade

echo "starting app..." && exec gunicorn --config /app/gunicorn_config.py run:app
