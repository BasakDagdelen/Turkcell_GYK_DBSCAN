from sqlalchemy import create_engine

def get_engine():
    user = 'postgres'
    password = "12345"
    host = 'localhost'
    port = 5432
    database = 'Gyk1Nortwind'
    return create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')
