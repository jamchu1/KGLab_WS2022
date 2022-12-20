from lodstorage.sql import SQLDB, EntityInfo
from KGLab_WS2022.table import Table
from KGLab_WS2022.series import Series
from KGLab_WS2022.series import fromDBSeries
from KGLab_WS2022.past_event import fromDBEvent

from lodstorage.sparql import SPARQL
import os

'''
Created on 2021-08-21

@author: wf
'''
import os
import urllib
import gzip
import shutil
import time

class Download:
    '''
    Utility functions for downloading data
    '''
    
    @staticmethod
    def getURLContent(url:str):
        with urllib.request.urlopen(url) as urlResponse:
            content = urlResponse.read().decode()
            return content

    @staticmethod
    def getFileContent(path:str):
        with open(path, "r") as file:
            content = file.read()
            return content

    @staticmethod
    def isEmpty(filePath:str,force:bool=False)->bool:
        '''
        check if a download of the given filePath is necessary that is the file
        does not exist has a size of zero or the download should be forced
        
        Args:
            filePath(str): the path of the file to be checked
            force(bool): True if the result should be forced to True
            
        Return:
            bool: True if  a download for this file needed
        '''
        if not os.path.isfile(filePath):
            result=True
        else:
            stats=os.stat(filePath)
            size=stats.st_size
            result=force or size==0
        return result

class DatabaseUtils:

    @staticmethod
    def extract_events(dbfile="KGLab_WS2022/databases/EventCorpus.db", cachefile="KGLab_WS2022/databases/event.db"):
        # create new table
        sqlDB = SQLDB(cachefile, debug=True, errorDebug=True)
        if Download.isEmpty(cachefile):
            # create cachefile
            if not os.path.isfile(dbfile):
                # TODO download DB file
                raise Exception(f"dbfile {dbfile} does not exist!")
            
            # Create a SQL connection to our SQLite database 
            cc_sqlDB = SQLDB(dbfile)

            # store data in cachefile
            DatabaseUtils.cacheDBHelper(oldDB=cc_sqlDB,newDB=sqlDB,entityName="eventseries_wikidata",query=
                "SELECT eventSeriesId, acronym, title, homepage FROM eventseries_wikidata WHERE homepage IS NOT NULL"
            )
            DatabaseUtils.cacheDBHelper(oldDB=cc_sqlDB,newDB=sqlDB,entityName="eventseries_or",query=
                "SELECT acronym, title, homepage FROM eventseries_or WHERE homepage IS NOT NULL"
            )
            DatabaseUtils.cacheDBHelper(oldDB=cc_sqlDB,newDB=sqlDB,entityName="event_wikidata",query=
                "SELECT eventInSeriesId, eventTitle as title, location, country, startDate, endDate, year, language, homepage FROM event_wikidata"
            )
            DatabaseUtils.cacheDBHelper(oldDB=cc_sqlDB,newDB=sqlDB,entityName="event_or",query=
                "SELECT inEventSeries, title, country, startDate, endDate, year, homepage FROM event_or"
            )
            cc_sqlDB.close()

        # construct table
        table = Table([])
        # wikidata
        entityInfo = EntityInfo([],"eventseries_wikidata", primaryKey=None)
        wdSeriesList = sqlDB.queryAll(entityInfo)
        for seriesEntry in wdSeriesList:
            events = sqlDB.query("SELECT * FROM event_wikidata WHERE eventInSeriesId = '" + seriesEntry["eventSeriesId"] + "'")
            series = fromDBSeries(seriesEntry)
            for event in events:
                series.eventList.append(fromDBEvent(event))
            table.eventseriesList.append(series)
        # open research
        entityInfo = EntityInfo([],"eventseries_or", primaryKey=None)
        orSeriesList = sqlDB.queryAll(entityInfo)
        for seriesEntry in orSeriesList:
            events = sqlDB.query("SELECT * FROM event_or WHERE inEventSeries = '" + seriesEntry["acronym"] + "'")
            series = fromDBSeries(seriesEntry)
            for event in events:
                series.eventList.append(fromDBEvent(event))
            table.eventseriesList.append(series)

        return table

    @staticmethod
    def cacheDBHelper(oldDB, newDB, query, entityName):
        data = oldDB.query(query)
        entityInfo=newDB.createTable(data,entityName=entityName,primaryKey=None)
        newDB.store(data,entityInfo,executeMany=True,fixNone=True)
