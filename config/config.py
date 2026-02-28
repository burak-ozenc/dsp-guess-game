import os
from dotenv import load_dotenv, dotenv_values
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")

class Config:
    BULK_COPY_SIZE = 100
    TOTAL_FILE_LIMIT_TO_PROCESS = 2000
    
    @property
    def CONNECTION_STRING(self):
        return os.getenv('CONNECTION_STRING')

    @property
    def DATA_ROOT_PATH(self):
        return os.getenv('DATA_ROOT_PATH')

config = Config()