import os

DATABASE = os.environ.get("MONGODB_DATABASE", "interview")
USERNAME = os.environ.get("MONGODB_USERNAME", "interview")
PASSWORD = os.environ.get("MONGODB_PASSWORD", "interview")
HOSTNAME = os.environ.get("MONGODB_HOSTNAME", "localhost")
PORT = os.environ.get("MONGODB_PORT", 27017)

MONGOURI = f"mongodb://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}"
