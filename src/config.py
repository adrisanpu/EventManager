from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")

#Cognito Confirgurations
COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN_ENDPOINT = f"{COGNITO_DOMAIN}/oauth2/token"

# S3 Configurations
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_REGION = os.getenv("S3_REGION")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")