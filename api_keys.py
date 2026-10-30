import os
from dotenv import load_dotenv

load_dotenv()

NVIDIA_NIM_API_KEY = os.getenv("NVIDIA_NIM_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/mrg")

IS_SANDBOX = not (NVIDIA_NIM_API_KEY and DEEPSEEK_API_KEY)
