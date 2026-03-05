# config/gunicorn.conf.py
import multiprocessing
import os

# Worker configuration - កាត់បន្ថយ memory usage
workers = 2  # កុំឲ្យច្រើនពេក (free tier មាន 512MB)
threads = 4
worker_class = "gthread"  # Use threads instead of processes

# Timeout settings - ការពារ slow requests
timeout = 30  # កាត់បន្ថយពី 120s (default) មក 30s
graceful_timeout = 30
keep_alive = 5

# Memory optimization
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# File upload limits - ការពារ crash
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

def when_ready(server):
    print("Gunicorn is ready!")