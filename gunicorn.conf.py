import os

# Render and cloud hosting port binding
port = os.environ.get("PORT", "5000")
bind = f"0.0.0.0:{port}"

# Concurrency & Worker configuration
workers = int(os.environ.get("WEB_CONCURRENCY", "2"))
threads = int(os.environ.get("PYTHON_THREADS", "2"))
timeout = int(os.environ.get("WEB_TIMEOUT", "120"))
accesslog = "-"
errorlog = "-"
loglevel = "info"
