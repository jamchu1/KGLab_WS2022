import lodstorage
from lodstorage.sql import SQLDB, EntityInfo

from lodstorage.sparql import SPARQL

class DatabaseUtils:

    @staticmethod
    def readDB():
        # creating file path
        dbfile = 'ConferenceCorpus\EventCorpus.db'
        # Create a SQL connection to our SQLite database 
        sqlDB = SQLDB(dbfile)

        # reading all table names
        #table_list = [a for a in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]

        event_list = []

        for sqlQuery in ["SELECT acronym, homepage FROM eventseries_wikidata WHERE homepage IS NOT NULL",
          "SELECT acronym, homepage FROM eventseries_or WHERE homepage IS NOT NULL"]:
          subList = sqlDB.query(sqlQuery)
          event_list.extend(subList)

        sqlDB.close()


        #create new table
        sqlDB = SQLDB("/tmp/event.db", debug=True, errorDebug=True)

        entityInfo=sqlDB.createTable(event_list[:10],entityName="event",primaryKey=None)
        sqlDB.store(event_list,entityInfo,executeMany=True,fixNone=True)

        return event_list