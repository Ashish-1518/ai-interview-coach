"""Gunicorn configuration for production.

Gunicorn manages multiple Uvicorn worker processes so the app can handle
concurrent requests and automatically restart crashed workers.

Usage:
    gunicorn -c gunicorn.conf.py app.main:app
"""

import multiprocessing
import os

# --------------------------------------------------------------------------- #
# Server socket
# --------------------------------------------------------------------------- #

# Render (and many PaaS) inject a PORT env var.  Fall back to 8000 for local
# docker-compose usage.
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

# --------------------------------------------------------------------------- #
# Workers
# --------------------------------------------------------------------------- #

# Uvicorn workers for async FastAPI.
worker_class = "uvicorn.workers.UvicornWorker"

# Rule of thumb: (2 × CPU cores) + 1.  On Render free tier (0.1 CPU) this
# resolves to 1, which is fine — the single async worker still handles many
# concurrent I/O-bound requests.
workers = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2 + 1))

# --------------------------------------------------------------------------- #
# Timeouts
# --------------------------------------------------------------------------- #

# Graceful timeout — how long a worker has to finish serving its current
# request after receiving a restart signal.
graceful_timeout = 120

# Worker timeout — kill and restart workers that are silent for this long.
# Set high because AI evaluation calls can be slow.
timeout = 120

# Keep-alive — how long to wait for the next request on a keep-alive
# connection before closing it.
keepalive = 5

# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #

# Use "-" to send to stdout/stderr (container-friendly).
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info").lower()
