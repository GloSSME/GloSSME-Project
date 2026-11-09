from django.db import connections
import os
import uuid
from django.conf import settings
from django.utils.text import get_valid_filename

def fnFetchDetailsWithCategoryID(       nLanguageID
                                    ,   nCommonValueCategoryID
                                ):

    cStrSQL     =   """
                        SELECT        
                                        nCommonValuesID
                                    ,   nLanguageID
                                    ,   cCommenValueName
                                    ,   nCommonValueCategoryID 
                            FROM        CommonValues
                            WHERE       nLanguageID                 =   %s 
                            AND         nCommonValueCategoryID      =   %s
                    """

    dsCommonDetails     =   fnPublicFetchAll(   cStrSQL
                                                ,   [       nLanguageID
                                                        ,   nCommonValueCategoryID
                                                    ]
                                                ,   'central'

                                            )
    lstCommonDetails    =   [
                                {
                                        'nCommonValuesID'               :   row[0]
                                    ,   'nLanguageID'                   :   row[1]
                                    ,   'cCommenValueName'              :   row[2]
                                    ,   'nCommonValueCategoryID'        :   row[3]
                                }       for row in dsCommonDetails
                        ]
    return lstCommonDetails

def fnSaveandUploadImageFile(cLogoPath, cFolderName):

    if hasattr(cLogoPath, 'read'):

        cFileName       =   get_valid_filename(cLogoPath.name)

        cFullPath       =   os.path.join(settings.MEDIA_ROOT, cFolderName, cFileName)

        with open(cFullPath, 'wb') as f:
            for chunk in cLogoPath.chunks():
                f.write(chunk)

        return cFileName

    return None


def fnSaveEditForm(     cStrSQL
                    ,   params      
                    ,   cDBName    
                    ,   bReturnID   =   False 
                ):

    dbconnection    =   connections[cDBName]

    try:
        with dbconnection.cursor() as cursor:
            
            cursor.execute(     cStrSQL
                            ,   params 
   
                        )

            if bReturnID:
                row         =   cursor.fetchone()
                nReturnID   =   row[0] if row else None
                dbconnection.commit()
                return nReturnID

            dbconnection.commit()

        return True

    finally:
        dbconnection.close()


def fnPublicFetchAll(       cStrSQL
                        ,   cParamValue
                        ,   cDBName    
                    ):

    dbconnection = connections[cDBName]

    try:
        with dbconnection.cursor() as cursor:
     
            cursor.execute(     cStrSQL
                            ,   cParamValue
                        )
  
            dctResult = cursor.fetchall()

        return dctResult

    finally:
        dbconnection.close()

def fnPublicFetchOne(       cStrSQL
                        ,   cParamValue
                        ,   cDBName    
                    ):

    dbconnection    =   connections[cDBName]

    try:
        with dbconnection.cursor() as cursor:
     
            cursor.execute(     cStrSQL
                            ,   cParamValue
                        )
  
            dctResult = cursor.fetchone()

        return dctResult

    finally:
        dbconnection.close()
    
def fnPublicFetchAllNoParam(        cStrSQL
                                ,   cDBName    
                            ):


    dbconnection = connections[cDBName]

    try:
        with dbconnection.cursor() as cursor:
     
            cursor.execute(     cStrSQL
                            )
  
            dctResult = cursor.fetchall()

        return dctResult

    finally:
        dbconnection.close()

def fnChkValue(         cColumnName
                    ,   cTableName
                    ,   cColumnValue
                    ,   cDBName  
                      
                ):

    cStrSQL     = f"""
                        IF EXISTS (
                                    SELECT 1 FROM {cTableName} WHERE {cColumnName} = %s
                                ) 
                                    
                            SELECT 1    AS IsExists
                        
                        ELSE
                           
                            SELECT 0    AS IsExists
                                    
                """

    dBConn = connections[cDBName]

    with dBConn.cursor() as cursor:
        
        cursor.execute(cStrSQL, [cColumnValue])
        nResultValue    =   cursor.fetchone()
    
    return nResultValue



def fnPublicDataGroupBy(    cStrSQL
                        ,   cParamValue
                        ,   cDBName    
                    ):

    dbConn = connections[cDBName]

    try:
        with dbConn.cursor() as cursor:

            cursor.execute(
                                cStrSQL
                            ,   cParamValue
                        )

            cHeaderColumns  =   [column[0] for column in cursor.description]
            cRowValues      =   cursor.fetchall()

        return cHeaderColumns, cRowValues

    finally:
        
        dbConn.close()