#!/bin/bash

# Not ideal but it works for now
sleep 5

python -m alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000

