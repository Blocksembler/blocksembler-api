import os

ORIGINS = os.environ.get("BLOCKSEMBLER_ORIGINS", "*").split(',')
BASE_URL = os.environ.get('BLOCKSEMBLER_API_BASE_URL', '')
MESSAGE_QUEUE_URL = os.environ.get('BLOCKSEMBLER_MESSAGE_QUEUE_URL', 'localhost')
MESSAGE_QUEUE_USER = os.environ.get('BLOCKSEMBLER_MESSAGE_QUEUE_USER', 'blocksembler')
MESSAGE_QUEUE_PASSWORD = os.environ.get('BLOCKSEMBLER_MESSAGE_QUEUE_PASSWORD', 'blocksembler')
DEBUG = os.environ.get('DEBUG', 'true').lower() == 'true'
DATABASE_URL = os.getenv("BLOCKSEMBLER_DB_URI", "postgresql+asyncpg://postgres:postgres@localhost:5432/blocksembler")
