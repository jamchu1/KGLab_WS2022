from lodstorage.sql import SQLDB, EntityInfo
from table import Table
from series import Series
from series import fromDBSeries
from past_event import fromDBEvent
from pathlib import Path

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

    @staticmethod
    def downloadAndExtract(url, filenameExt, targetPath):
        urllib.request.urlretrieve(url, targetPath + "." + filenameExt)
        with gzip.open(targetPath + "." + filenameExt, 'rb') as gzipped:
            with open(targetPath, 'wb') as unzipped:
                shutil.copyfileobj(gzipped, unzipped)
        os.remove(targetPath + "." + filenameExt)
        if not os.path.isfile(targetPath):
            raise (f"could not extract file from {targetPath}.{filenameExt}")

class DatabaseUtils:
    
    dbURL = "https://confident.dbis.rwth-aachen.de/downloads/conferencecorpus/EventCorpus.db.gz"
    dbFileExt = "gz"

    @staticmethod
    def extract_events(dbfilePath="KGLab_WS2022/databases/EventCorpus.db", cachefilePath="KGLab_WS2022/databases/event.db"):
        # create folder if not exists
        Path("KGLab_WS2022/databases").mkdir(parents=True, exist_ok=True)
        # create cachefile
        sqlDB = SQLDB(cachefilePath, debug=True, errorDebug=True)
        if Download.isEmpty(cachefilePath):
            # create cachefile
            if not os.path.isfile(dbfilePath):
                # download the database
                Download.downloadAndExtract(DatabaseUtils.dbURL, DatabaseUtils.dbFileExt, dbfilePath)
            # Create a SQL connection to our SQLite database 
            cc_sqlDB = SQLDB(dbfilePath)

            # store data in cachefile
            DatabaseUtils.cacheDBHelper(oldDB=cc_sqlDB,newDB=sqlDB,entityName="eventseries_wikidata",query=
                "SELECT eventSeriesId, acronym, title, homepage FROM eventseries_wikidata WHERE homepage IS NOT NULL"
            )
            DatabaseUtils.cacheDBHelper(oldDB=cc_sqlDB,newDB=sqlDB,entityName="eventseries_or",query=
                "SELECT acronym, title, homepage FROM eventseries_or WHERE homepage IS NOT NULL"
            )
            DatabaseUtils.cacheDBHelper(oldDB=cc_sqlDB,newDB=sqlDB,entityName="event_wikidata",query=
                "SELECT eventInSeriesId, eventTitle as title, location, country, startDate, endDate, year, language, homepage, ordinal FROM event_wikidata"
            )
            DatabaseUtils.cacheDBHelper(oldDB=cc_sqlDB,newDB=sqlDB,entityName="event_or",query=
                "SELECT inEventSeries, title, country, startDate, endDate, year, homepage, ordinal FROM event_or"
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
