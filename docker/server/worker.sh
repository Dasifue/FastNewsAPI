#!/bin/sh

exec celery -A app.src.celery.celery_app worker --loglevel=info