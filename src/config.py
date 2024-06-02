import os
import uuid

import dotenv


dotenv.load_dotenv()


HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', 8000))

DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_DATABASE = os.getenv('DB_DATABASE', 'postgres')
DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'

GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')

# Random secret if not passed
JWT_ACCESS_TOKEN_SECRET = os.getenv('JWT_ACCESS_TOKEN_SECRET', uuid.uuid4().hex)

LNBITS_BASE_URL = os.getenv('LNBITS_BASE_URL')
LNBITS_INVOICE_KEY = os.getenv('LNBITS_INVOICE_KEY')
LNBITS_CALLBACK_SECRET = os.getenv('LNBITS_CALLBACK_SECRET', uuid.uuid4().hex)
