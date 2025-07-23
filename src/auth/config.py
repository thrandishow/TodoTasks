from os import getenv

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY",None)
ALGORITHM = getenv("ALGORITHM",None)

CLIENT_ID = getenv("CLIENT_ID",None)
CLIENT_SECRET = getenv("CLIENT_SECRET",None)

