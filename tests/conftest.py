import os

# core.config needs these at import time; unit tests never connect to MongoDB
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017")
os.environ.setdefault("MONGO_DB_NAME", "nepal_legal_rag_test")
