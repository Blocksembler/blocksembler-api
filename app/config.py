import os

DEBUG = os.environ.get('DEBUG', 'true').lower() == 'true'
ORIGINS = os.environ.get("BLOCKSEMBLER_ORIGINS", "*").split(',')
BASE_URL = os.environ.get('BLOCKSEMBLER_API_BASE_URL', '')

DATABASE_URL = os.environ.get("BLOCKSEMBLER_DB_URI",
                              "postgresql+asyncpg://postgres:postgres@localhost:5432/blocksembler")

MQ_URL = os.environ.get('BLOCKSEMBLER_MQ_URL', 'localhost')
MQ_PORT = os.environ.get('BLOCKSEMBLER_MQ_PORT', '5672')
MQ_USER = os.environ.get("BLOCKSEMBLER_MQ_USER", "blocksembler")
MQ_PWD = os.environ.get("BLOCKSEMBLER_MQ_PWD", "blocksembler")

MQ_EXCHANGE_NAME = os.environ.get("BLOCKSEMBLER_MQ_EXCHANGE_NAME", "blocksembler-grading-exchange")
GRADING_JOB_QUEUE = os.environ.get('BLOCKSEMBLER_MQ_GRADING_JOB_QUEUE', "grading-jobs")
GRADING_JOB_ROUTING_KEY = os.environ.get('BLOCKSEMBLER_MQ_GRADING_JOB_ROUTING_KEY', 'grading.job.created')
