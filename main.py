import pandas as pd
from engine import recommend
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:root@localhost/books')

explicit_ratings = pd.read_sql('SELECT * FROM explicit_ratings', engine)

recommend(276747, explicit_ratings)

