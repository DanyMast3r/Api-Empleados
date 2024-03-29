from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from ..config.db import meta, engine


users = Table("Datos", meta, 
    Column("id", Integer, primary_key=True), 
    Column("calname", String(255)), 
    Column("username", String(255)), 
    Column("comentario", String(255)), 
    Column("calificacion", String(255)))

meta.create_all(engine)
