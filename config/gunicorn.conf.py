# config/gunicorn.conf.py
import os

# Worker configuration
workers = 2
threads = 4
worker_class = "gthread"

# Timeout settings - INCREASED significantly
timeout = 300  # 5 នាទី (ពី 120)
graceful_timeout = 300
keep_alive = 10

# Memory optimization - REDUCED to prevent memory issues
max_requests = 100  # កាត់ពី 500 មក 100
max_requests_jitter = 20
preload_app = True

# File upload limits
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "warning"

def when_ready(server):
    print("Gunicorn is ready!")