#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run the application
if [ "$ENVIRONMENT" = "production" ]; then
    # Production: Use Gunicorn with single worker for 512MB RAM limit
    gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker --timeout 120 app.main:app
else
    # Development: Use Uvicorn with reload
    uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload
fi
