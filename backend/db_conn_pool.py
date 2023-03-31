from psycopg2 import Error, pool
import os
from decouple import config
import logging


logging.basicConfig(level=logging.DEBUG, filename='app.log',
                    format="%(asctime)s - %(levelname)s - %(message)s", datefmt='%d-%m-%Y %H:%M:%S')


try:
    DATABASE_HOST = config('DATABASE_HOST')
    DATABASE_NAME = config('DATABASE_NAME')
    DATABASE_USER = config('DATABASE_USER')
    DATABASE_PASSWORD = config('DATABASE_PASSWORD')
    DATABASE_PORT = config('DATABASE_PORT')
    DATABASE_MINCONN = config('DATABASE_MINCONN')
    DATABASE_MAXCONN = config('DATABASE_MAXCONN')
    logging.info("ENV variables ready")
except (Exception, KeyError) as e:
    logging.error('Missing environment variable: %s', e)


def getConnPool():
    try:
        conn = pool.SimpleConnectionPool(
            host=DATABASE_HOST,
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            port=DATABASE_PORT,
            minconn=DATABASE_MINCONN,
            maxconn=DATABASE_MAXCONN
        )
        logging.info("Connected to DB")
        return conn
    except (Exception, Error) as error:
        logging.error('Database connection error: %s', error)
