from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import logging
# import os

env_path = './config.env'
load_dotenv(dotenv_path=env_path)

logging.info(str("  =====>  ") + str(os.environ.get("user")))
logging.info(str("  =====>  ") + str(os.environ.get("host")))


engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(os.environ.get("user"), os.environ.get("password"),
                                                                   os.environ.get("host"),
                                                                   os.environ.get("port"),
                                                                   os.environ.get("database")))