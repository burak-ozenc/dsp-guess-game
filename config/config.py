import os
from dotenv import load_dotenv, dotenv_values
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    S3_BUCKET = os.getenv("S3_BUCKET")
    S3_REGION = os.getenv("S3_REGION")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    PRESIGNED_URL_EXPIRY = 300
    BULK_COPY_SIZE = 25
    TOTAL_FILE_LIMIT_TO_PROCESS = 1000
    DEFAULT_SAMPLE_DURATION_IN_SECONDS = 30
    DEFAULT_SAMPLE_RATE = 16000
    HOP_LENGTH = 512
    N_FFT = 2048
    N_MFCC = 13

    @property
    def CONNECTION_STRING(self):
        return os.getenv('CONNECTION_STRING')

    @property
    def DATA_ROOT_PATH(self):
        return os.getenv('DATA_ROOT_PATH')


config = Config()
