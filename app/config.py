import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('POSTGRES_URL').replace('postgres://', 'postgresql+psycopg2://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False