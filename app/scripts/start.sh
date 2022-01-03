export APP_MODULE=${APP_MODULE-main:app}
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-80}

exec uvicorn --reload --host $HOST --port $PORT "$APP_MODULE"