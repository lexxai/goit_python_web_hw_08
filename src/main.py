
from hw.database.connect import connect_db
from hw.database.seeds import seeds



if connect_db():
    seeds()