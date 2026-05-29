import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APPWRITE_ENDPOINT: str = os.getenv('APPWRITE_ENDPOINT')
    APPWRITE_PROJECT_ID: str = os.getenv('APPWRITE_PROJECT_ID')
    APPWRITE_API_KEY: str = os.getenv('APPWRITE_API_KEY')

    DATABASE_ID: str = os.getenv('APPWRITE_DATABASE_ID')
    APPWRITE_USERS_COLLECTION_ID: str = os.getenv('APPWRITE_USERS_COLLECTION_ID')

settings = Settings()