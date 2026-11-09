from django.db import connections
from glossme.PublicFunctions        import *

def fnValidateDeviceDetails(        cManufacturer
                                ,   cDeviceModel
                                ,   nDeviceTypeID
                                ,   cOSVersion
                                ,   cSDKVersion
                            ):

    cStrSQL     =   """     
                        SELECT   
                                [nDeviceModelMasterID]
                        FROM    [DeviceModelDetails]
                        WHERE   cManufacturer   =   %s
                        AND     cDeviceModel    =   %s
                        AND     nDeviceTypeID   =   %s
                        AND     cOSVersion      =   %s
                        AND     cSDKVersion     =   %s
  
                    """
    dtResult    =   fnPublicFetchOne(       cStrSQL
                                        ,   [       cManufacturer
                                                ,   cDeviceModel
                                                ,   nDeviceTypeID
                                                ,   cOSVersion
                                                ,   cSDKVersion
                                            ]
                                        ,   'PublicFacing'
                                    )
    if dtResult is None:

        cStrSQL =   """
                        EXEC        [spInsertDeviceModels]
                                    @cManufacturer      =   %s,
                                    @cDeviceModel       =   %s,
                                    @nDeviceTypeID      =   %s,
                                    @cOSVersion         =   %s,
                                    @cSDKVersion        =   %s
                    """
        nReturnValueID  =   fnSaveEditForm(
                                            cStrSQL
                                            ,   [
                                                        cManufacturer
                                                    ,   cDeviceModel
                                                    ,   nDeviceTypeID
                                                    ,   cOSVersion
                                                    ,   cSDKVersion
                                                ]
                                            ,   'PublicFacing'
                                            ,   True

                                        )


        return nReturnValueID

    return dtResult[0]

