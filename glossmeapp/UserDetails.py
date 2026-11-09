import  json

from    django.conf                    import  settings
from    glossme.PublicFunctions        import  *



def fnReturnUserDetails(    nUserMasterID    =   0
                        ,   nLanguageID     =   0
                        ,   cName           =   ''
                        ,   cPhoneNo        =   ''
                        ):

    tuParameters    =   []

    cStrSQL     =   """
                         SELECT
                                        [nUserMaterID]              -- 0
                                    ,   [cProfilePicture]           -- 1
                                 
                                    ,   [cFullName]                 -- 4
                                    ,   [dDoB]                      -- 5
                                    ,   [nGenderID]                   -- 6
                                    ,   [cGenderName]               -- 7
                                    ,   [cAddress]                  -- 8
                                
                                    ,   [cPhoneNumber]              -- 10
                                
                                    ,   [nIdTypeID]                 -- 12
                                    ,   [cIdCardNumber]             -- 13
                                    ,   [nLat]                 -- 14
                                    ,   [nLong]                -- 15
                                    ,   [gUserLocation]                -- 16
                                    ,   [nLanguageID]                -- 17
                                    ,   [cLanguageName]             -- 18
                              
                                    ,   [nUserTypeID]      -- 19

                                    ,   [dDoC]                      -- 20
                                    ,   [dDoM]                      -- 21
                            FROM        [ViewUserMasterDetails]
                            WHERE       1   =   1
                     """

    if int(nUserMasterID)    >   0:
        cStrSQL         +=  "   AND   nUserMasterID   =   %s"
        tuParameters.append(nUserMasterID)

    if int(nLanguageID)      >   0:
        cStrSQL         +=  "   AND   nLanguageID   =   %s"
        tuParameters.append(nLanguageID)

    if cName                !=  '':
        cStrSQL         +=  "   AND   cFullName   LIKE   %s"
        tuParameters.append(f"{cName}%")

    if cPhoneNo             !=  '':
        cStrSQL         +=  "   AND   cPhoneNumber   =   %s"
        tuParameters.append(f"{cPhoneNo}")

    cStrSQL             +=  "   ORDER BY     cFullName"
    tuParameters        =   tuple(tuParameters)

    dsUserDetails       =   fnPublicFetchAll (      cStrSQL
                                                ,   tuParameters
                                                ,   'default'
                                            )

    if dsUserDetails:

        lstUserDetails  =   [{

                                        'nUserMaterID'          :   row[0]
                                 ,   'cProfilePicture'   :   f"{settings.AUDIO}{settings.MEDIA_URL}User/ProfilePics/{row[1]}" if row[1] else ""
                                    
                                    ,   'cFullName'            :   row[2]
                              
                                 
                                    ,   'dDoB'                  :   str(row[3]) if row[3] else ""
                                    ,   'nGenderID'               :   row[4]
                                    ,   'cGenderName'           :   row[5]
                                    ,   'cAddress'              :   row[6]
                               
                                    ,   'cPhoneNumber'          :   row[7]
                                
                                    ,   'nIdTypeID'             :   row[8]
                                    ,   'cIdCardNumber'         :   row[9]
                                    ,   'nLat'             :   float(row[10]) if row[10] is not None else None
                                    ,   'nLong'            :   float(row[11]) if row[11] is not None else None
                                    ,   'gUserLocation'            :   row[12]
                                    ,   'nLanguageID'            :   row[13]
                                    ,   'cLanguageName'         :   row[14]
                                    # ,   'cIdCardDocumentImage'  :   f"{settings.AUDIO}/{settings.MEDIA_ROOT}/User/IDDocs/{row[15]}" if row[15] else ""
                                    ,   'nUserTypeID'         :   row[15]

                                    ,   'dDoC'                  :   str(row[16]) if row[16] else ""
                                    ,   'dDoM'                  :   str(row[17]) if row[17] else ""
                            }       for row in dsUserDetails
                        ]
        return  lstUserDetails
    else:
        return  False


def fnVerifyInstallation(       nUserID
                            ,   nUserTypeID
                         
                        ):
    
    cStrSQL   =   """
                        SELECT  nUserDeviceMasterID
                            ,   nDeviceModelMasterID
                            ,   cManufacturer
                            ,   cDeviceModel

                        FROM    viewUserDeviceMasterDetails
                        WHERE   nUserID             =   %s
                        AND     nUserTypeID         =   %s
                      
              """
    

    dtResult = []

    dtResult    =   fnPublicFetchAll(           cStrSQL
                                        ,[      nUserID
                                            ,   nUserTypeID
                                          
                                        ]
                                            ,   'default'
                                    )

    if dtResult:
        lstResult   =   [
                        {       'nUserDeviceMasterID'   :   dtValue[0]
                            ,   'nDeviceModelMasterID'  :   dtValue[1]
                            ,   'cManufacturer'         :   dtValue[2]
                            ,   'cDeviceModel'          :   dtValue[3]
                        }       for dtValue in dtResult
                    ]
        return lstResult
    else:
        return None

from django.db import connections


def fnAddUserMasterDetails(
                                nLanguageID
                            ,   cFirstName
                            ,   cLastName
                            ,   dDoB
                            ,   nGenderID
                            ,   cAddress
                            ,   cPhoneNumber
                            ,   nIDTypeID
                            ,   cIDCardNumber
                            ,   nLat
                            ,   nLong
                            ,   cProfilePicture
                            ,   nUserTypeID
                                    ,   iMode

                        ):

    cStrSQL     =   """
                     

                        EXEC	[InsertUserMasterDetails]
                                @nLanguageID         =   %s,
                                @cFirstName         =   %s,
                                @cLastName          =   %s,
                                @dDoB               =   %s,
                                @nGenderID          =   %s,
                                @cAddress           =   %s,
                                @cPhoneNumber       =   %s,
                                @nIDTypeID          =   %s,
                                @cIDCardNumber      =   %s,
                                @nLat               =   %s,
                                @nLong              =   %s,
                                @cProfilePicture    =   %s,
                                @nUserTypeID        =   %s,
                                @iMode					=	%s
                                
                    """

    fnSaveEditForm(         cStrSQL
                        ,   [
                                nLanguageID
                            ,   cFirstName
                            ,   cLastName
                            ,   dDoB
                            ,   nGenderID
                            ,   cAddress
                            ,   cPhoneNumber
                            ,   nIDTypeID
                            ,   cIDCardNumber
                            ,   nLat
                            ,   nLong
                            ,   cProfilePicture
                            ,   nUserTypeID
                            ,   iMode

                        ]
                        ,       'default'
                        )

    return True


def fnSaveUserDeviceMasterDetails(
                                        nUserDeviceMasterID
                                    ,   nLanguageID
                                    ,   cTelephoneNo
                                    ,   cDeviceUUID
                                    ,   nDeviceTypeID
                                    ,   nDeviceModelMasterID
                                    ,   nUserTypeID
                                    ,   nUserID
                                  
                                    ,   cFCMToken
                                    ,   nLat
                                    ,   nLong
                                    ,   iMode
                                ):
        
    cStrSQL     =   """
                        EXEC	[spInsertUpdateUserDeviceMaster]
                                @nUserDeviceMasterID    =   %s,
                                @nLanguageID			=	%s,
                                @cTelephoneNo			=	%s,
                                @cDeviceUUID            =   %s,
                                @nDeviceTypeID			=	%s,
                                @nDeviceModelMasterID	=	%s,
                                @nUserTypeID			=	%s,
                                @nUserID				=	%s,
                               
                                @cFCMToken				=	%s,
                                @nLat					=	%s,
                                @nLong					=	%s,
                                @iMode					=	%s
                    """

    fnSaveEditForm(         cStrSQL
                        ,   [
                                nUserDeviceMasterID
                            ,   nLanguageID
                            ,   cTelephoneNo
                            ,   cDeviceUUID
                            ,   nDeviceTypeID
                            ,   nDeviceModelMasterID
                            ,   nUserTypeID
                            ,   nUserID
                        
                            ,   cFCMToken
                            ,   nLat
                            ,   nLong
                            ,   iMode
                        ]
                        ,       'default' 
                        )
    
    return True


def fnGetUserByPhoneNumber(cPhoneNumber):

    cStrSQL     =   """
                        SELECT
                                    nUserMaterID
                                ,   nUserTypeID
                                ,   cPhoneNumber
                        FROM        UserMasterDetails
                        WHERE       cPhoneNumber = %s
                    """

    dtResult    =   fnPublicFetchAll(
                                cStrSQL
                            ,   (cPhoneNumber,)
                            ,   'default'
                        )

    if dtResult:
        return {
                    'nUserMaterID'  :   dtResult[0][0]
                ,   'nUserTypeID'   :   dtResult[0][1]
                ,   'cPhoneNumber'  :   dtResult[0][2]
                }

    return None


def fnUpdateUserTypeID(nUserMaterID, nUserTypeID):

    cStrSQL     =   """
                        UPDATE      UserMasterDetails
                        SET         nUserTypeID = %s
                        WHERE       nUserMaterID = %s
                    """

    fnSaveEditForm(
                        cStrSQL
                    ,   [
                                nUserTypeID
                            ,   nUserMaterID
                        ]
                    ,   'default'
                )

    return True

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
                                ,   json.dumps(lstDescriptions, ensure_ascii=False)
                                ,   json.dumps(lstImages, ensure_ascii=False)
                                ,   iMode
                            ]
                            ,   'default'
                            ,   bReturnID   =   True
                        )



