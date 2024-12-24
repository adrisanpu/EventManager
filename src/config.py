from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
API_BASE_URL = os.getenv("API_BASE_URL")
TOKEN_ENDPOINT = f"{COGNITO_DOMAIN}/oauth2/token"