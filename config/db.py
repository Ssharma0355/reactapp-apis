from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Use Atlas connection string
MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://t8540895_db_user:bboFupS7Jn5BeSYv@cluster0.uiabdvg.mongodb.net/?retryWrites=true&w=majority"
)

# Force TLS/SSL to avoid handshake errors
client = MongoClient(MONGO_URL, tls=True, tlsAllowInvalidCertificates=True)

# Use your DB name
db = client["mydatabase"]

# Define the collection explicitly
users_collection = db["users"]
