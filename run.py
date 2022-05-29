#!/usr/bin/python3
from app import app
import os

host = os.environ.get("HOST", "127.0.0.1")
port = int(os.environ.get("PORT", 5000))
environment = os.environ.get("ENVIRONMENT", "dev")
print(f"Host: {host}")
print(f"Port: {port}")
print(f"Environment: {environment}")
app.run(debug=(environment == "dev"), port=port, host=host)
