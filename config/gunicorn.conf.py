# config/gunicorn.conf.py
import multiprocessing
import os

# Bind to the platform-provided port (DigitalOcean/Railway set $PORT; default 8080)
bind = "0.0.0.0:" + os.getenv("PORT", "8080")

# Worker configuration
workers = 2
threads = 4
worker_class = "gthread"

# Timeout settings - INCREASED for image processing
timeout = 120  # raised from 30 to 120 seconds
graceful_timeout = 120
keep_alive = 5

# Memory optimization
max_requests = 500  # reduced from 1000 to 500
max_requests_jitter = 50
preload_app = True

# File upload limits
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

def when_ready(server):
    print("Gunicorn is ready!")