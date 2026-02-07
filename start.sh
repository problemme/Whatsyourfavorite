#!/usr/bin/env bash

echo "Starting FastAPI app..."

uvicorn back_end.app:app --host 0.0.0.0 --port ${PORT:-8000}
