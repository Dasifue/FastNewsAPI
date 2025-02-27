#!/bin/sh

alembic upgrade head

exec fastapi run --host 0.0.0.0 --port 8000