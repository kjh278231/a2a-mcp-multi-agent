import os
import dotenv

dotenv.load_dotenv()

OPENAI_API_KEY: str = str(os.getenv("OPENAI_API_KEY"))
GOOGLE_API_KEY: str = str(os.getenv("GOOGLE_API_KEY"))
