
from hw08.database.connect import connect_db
from hw08.database.seeds import seeds



if connect_db():
    seeds()