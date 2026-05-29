from app.config.settings import settings
from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.services.account import Account
from appwrite.services.databases import Databases
from appwrite.services.tables_db import TablesDB
from appwrite.id import ID

client = Client()
client.set_endpoint(settings.APPWRITE_ENDPOINT)
client.set_project(settings.APPWRITE_PROJECT_ID)
client.set_key(settings.APPWRITE_API_KEY)

databases = Databases(client) # Database operations are now deprecated
tables_db = TablesDB(client)

# I'm using users service because I'm not initiating the auth directly from the frontend
users_service = Users(client)

account = Account(client)