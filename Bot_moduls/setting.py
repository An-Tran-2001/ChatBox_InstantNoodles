"""
Import libraries for load file and warnings notifical
"""

import dotenv
import os
import warnings
warnings.filterwarnings('ignore')

"""
Import env
"""

project_dir = os.path.join(os.path.dirname(__file__), os.pardir)
dotenv_path = os.path.join(project_dir, '.env')
dotenv.load_dotenv(dotenv_path)

ASTRA_DB_ID = os.environ.get('ASTRA_DB_ID')
ASTRA_DB_REGION = os.environ.get('ASTRA_DB_REGION')
ASTRA_DB_KEYSPACE = os.environ.get('ASTRA_DB_KEYSPACE')
ASTRA_DB_APPLICATION_TOKEN = os.environ.get('ASTRA_DB_APPLICATION_TOKEN')
PATH_SECURE_CONNECT_BUNDLE = f"{project_dir}/{str(os.environ.get('PATH_SECURE_CONNECT_BUNDLE'))}"
ASTRA_CLIENT_ID = os.environ.get('ASTRA_CLIENT_ID')
ASTRA_CLIENT_SECRET = os.environ.get('ASTRA_CLIENT_SECRET')