import lodstorage
import sqlite3

from lodstorage.sparql import SPARQL

class DatabaseUtils:

    @staticmethod
    def readDB():
        # creating file path
        dbfile = 'ConferenceCorpus\EventCorpus.db'
        # Create a SQL connection to our SQLite database 
        con = sqlite3.connect(dbfile)

        # creating cursor
        cur = con.cursor()

        # reading all table names
        #table_list = [a for a in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]

        event_list_wikidata = [a for a in cur.execute("SELECT acronym, homepage FROM eventseries_wikidata WHERE homepage IS NOT NULL")]
        event_list_or = [a for a in cur.execute("SELECT acronym, homepage FROM eventseries_or WHERE homepage IS NOT NULL")]
        #event_list_orclonebackup = [a for a in cur.execute("SELECT acronym, homepage FROM eventseries_orclonebackup WHERE homepage IS NOT NULL")]
        #event_list_orclone = [a for a in cur.execute("SELECT acronym, homepage FROM eventseries_orclone WHERE homepage IS NOT NULL")]
        #event_list_orbackup = [a for a in cur.execute("SELECT acronym, homepage FROM eventseries_orbackup WHERE homepage IS NOT NULL")]

        event_list = []

        for event in event_list_wikidata:
          if not event in event_list:
            event_list.append(event)

        for event in event_list_or:
          if not event in event_list:
            event_list.append(event)

        #for event in event_list:
        #  print(event)

        # Be sure to close the connection
        con.close()

        return event_list