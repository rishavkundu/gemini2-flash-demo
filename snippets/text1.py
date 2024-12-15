from google import genai
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()


client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY"),
    http_options={"api_version": "v1alpha"},
)
print("Connected to the AI model!")
