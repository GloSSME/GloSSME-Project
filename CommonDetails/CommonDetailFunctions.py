import  json

from    django.conf                    import  settings
from    glossme.PublicFunctions        import  *

def fnGetBrandList(cBrandName=None):
    print(cBrandName,"cBrandName")
    cstrSQL = """
                SELECT   TOP 500 [nBrandModelMasterID]
                        ,[cBrandName]
                FROM     [BrandModelMaster]
                WHERE    nStatusID              = 1
          
            """
    lstParams = []
    if cBrandName:
        cstrSQL += " AND cBrandName LIKE %s"
        lstParams.append(f"%{cBrandName}%")

    cstrSQL += " ORDER BY cBrandName"

    return fnPublicFetchAll(cstrSQL, lstParams, 'default')