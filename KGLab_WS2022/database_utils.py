import lodstorage
from lodstorage.sql import SQLDB, EntityInfo

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
    def extract_events(dbfile="databases/EventCorpus.db", cachefile="databases/event.db"):
        #create new table
        sqlDB = SQLDB(cachefile, debug=True, errorDebug=True)
        if Download.isEmpty(cachefile):
            if not os.path.isfile(dbfile):
                raise Exception(f"dbfile {dbfile} does not exist!")
            
            # Create a SQL connection to our SQLite database 
            cc_sqlDB = SQLDB(dbfile)

            # reading all table names
            #table_list = [a for a in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
    
            event_list = []
    
            for sqlQuery in ["SELECT acronym, homepage FROM eventseries_wikidata WHERE homepage IS NOT NULL",
              "SELECT acronym, homepage FROM eventseries_or WHERE homepage IS NOT NULL"]:
                subList = cc_sqlDB.query(sqlQuery)
                event_list.extend(subList)
    
            cc_sqlDB.close()

            entityInfo=sqlDB.createTable(event_list,entityName="event_series",primaryKey=None)
            sqlDB.store(event_list,entityInfo,executeMany=True,fixNone=True)
        else:
            sampleRecords=[
                {
                     "acronym": "ESWC",
                     "homepage": "http://eswc.xy"
                }]
            entityInfo=EntityInfo(sampleRecords,"event_series",primaryKey=None)
            event_list=sqlDB.queryAll(entityInfo)

        return event_list