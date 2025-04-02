import sqlalchemy
from langchain_community.utilities.sql_database import SQLDatabase

sql_engine = sqlalchemy.create_engine("sqlite:////Users/otisvaliant/Documents/codes/prushka/Chinook_Sqlite.sqlite")
sql_db = SQLDatabase(sql_engine)