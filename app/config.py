import os

class Config:
    app_settings = os.getenv('APP_SETTINGS', 'development')

    if app_settings == 'production':
        SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('PROD_POSTGRES_USER')}:" +
        f"{os.getenv('PROD_POSTGRES_PASSWORD')}@" +
        f"{os.getenv('PROD_POSTGRES_HOST')}:" +
        f"{os.getenv('PROD_POSTGRES_PORT')}/" +
        f"{os.getenv('PROD_POSTGRES_DB')}"
        )
    else: # development середовище
        SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('POSTGRES_USER')}:" +
        f"{os.getenv('POSTGRES_PASSWORD')}@" +
        f"localhost:5432/{os.getenv('POSTGRES_DB')}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False