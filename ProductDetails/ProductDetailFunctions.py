import  json

from    django.conf                    import  settings
from    glossme.PublicFunctions        import  *

def fnSaveServiceMasterDetails(
                                    nServiceMasterID
                                ,   nOrganizationID
                                ,   nBranchID
                                ,   nDepartmentID
                                ,   nCategoryID
                                ,   cServiceName
                                ,   cBrand
                                ,   cModelNo
                                ,   dManufacturingDate
                                ,   dWorkStartTime
                                ,   dWorkEndTime
                                ,   nOperationRangeYN
                                ,   nOperationRangeKms
                                ,   nStaffNeededYN
                                ,   nHolidayIncludedYN
                                ,   cQRCode
                                ,   nLat
                                ,   nLong
                                ,   lstDescriptions
                                ,   lstImages
                                ,   iMode
                            ):

    cStrSQL     =   """
                        EXEC	[spInsertUpdateServiceMasterDetails]
                                @nServiceMasterID       =   %s,
                                @nOrganizationID        =   %s,
                                @nBranchID              =   %s,
                                @nDepartmentID          =   %s,
                                @nCategoryID            =   %s,
                                @cServiceName           =   %s,
                                @cBrand                 =   %s,
                                @cModelNo               =   %s,
                                @dManufacturingDate     =   %s,
                                @dWorkStartTime         =   %s,
                                @dWorkEndTime           =   %s,
                                @nOperationRangeYN      =   %s,
                                @nOperationRangeKms     =   %s,
                                @nStaffNeededYN         =   %s,
                                @nHolidayIncludedYN     =   %s,
                                @cQRCode                =   %s,
                                @nLat                   =   %s,

                                @nLong                  =   %s,
                                
                                @cDescriptions          =   %s,
                                @cImages                =   %s,
                                @iMode                  =   %s
                    """

    return  fnSaveEditForm(     cStrSQL
                            ,   [
                                    nServiceMasterID
                                ,   nOrganizationID
                                ,   nBranchID
                                ,   nDepartmentID
                                ,   nCategoryID
                                ,   cServiceName
                                ,   cBrand
                                ,   cModelNo
                                ,   dManufacturingDate
                                ,   dWorkStartTime.strftime('%H:%M:%S')
                                ,   dWorkEndTime.strftime('%H:%M:%S')
                                ,   nOperationRangeYN
                                ,   nOperationRangeKms
                                ,   nStaffNeededYN
                                ,   nHolidayIncludedYN
                                ,   cQRCode
                                ,   nLat
                                ,   nLong
                                
                                ,   json.dumps(lstDescriptions, ensure_ascii=False)
                                ,   json.dumps(lstImages, ensure_ascii=False)
                                ,   iMode
                            ]
                            ,   'default'
                            ,   bReturnID   =   True
                        )