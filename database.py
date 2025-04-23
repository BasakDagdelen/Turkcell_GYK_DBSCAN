from sqlalchemy import create_engine

def get_engine():
    user = 'username'
    password = "password"
    host = 'localhost'
    port = 5432
    database = 'Gyk1Nortwind'
    return create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
