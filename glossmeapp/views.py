from django.shortcuts                       import  render
from rest_framework.decorators              import  api_view
from rest_framework.response                import  Response
from glossmeapp.serializers                 import  *
from rest_framework                         import  status
from glossmeapp.UserDetails                 import  *
from glossmeapp.PublicModules               import  *

@api_view(['POST'])

def fnCommonValues(request):

    nLanguageID             =   int(request.data.get("nLanguageID", 1))
    nCommonValueCategoryID  =   request.data.get("nCommonValueCategoryID")

    if nCommonValueCategoryID is not None:
        nCommonValueCategoryID  =   int(nCommonValueCategoryID)

    lstCommonValues   =   fnGetCommonValues(nLanguageID, nCommonValueCategoryID)

    return Response(
                        {
                            "status"    :   True,
                            "data"      :   lstCommonValues or []
                        },  status = 200
                    )

@api_view(['POST'])

def fnVerifyRegisteredMembers(request):
    
    if request.method       ==  "POST":
        
        szPhoneNo           =   PhoneSerializer(data  =   request.data)
        szDeviceInfo        =   DeviceSerializer(data  =   request.data)
        nLanguageID         =   request.data["nLanguageID"]
                
        bPhoneValid         =   szPhoneNo.is_valid()
        bDeviceValid        =   szDeviceInfo.is_valid()
        
        if not bPhoneValid or not bDeviceValid:
        
            return Response(
                                {
                                    "status"    :   False,
                                    "errors"    :   {
                                                        "Phone"     :   szPhoneNo.errors,
                                                        "Device"    :   szDeviceInfo.errors
                                                    }
                                },  status=400
            )

        cManufacturer   =   szDeviceInfo.validated_data["cManufacturer"]
        cDeviceModel    =   szDeviceInfo.validated_data["cDeviceModel"] 
        nDeviceTypeID   =   szDeviceInfo.validated_data["nDeviceTypeID"]
        cOSVersion      =   szDeviceInfo.validated_data["cOSVersion"]
        cSdkVersion     =   szDeviceInfo.validated_data["cSdkVersion"]

        cPhoneNumber    =   szPhoneNo.validated_data["cPhoneNumber"]
        nUserID         =   0
        nUserTypeID     =   0
        lstResult       =   []
           
# ****************--------- Check the person in the Database    ---------****************    

#     ----------------------  Check Member Details  ----------------------

        if (lstResult   := fnReturnUserDetails(
                                                            0
                                                        ,   nLanguageID    
                                                        ,   ''
                                                        ,   cPhoneNumber
                                                   
                                                    )
            ) or []:

            if len(lstResult)   ==  1:
                nNoofUsers      =   len(lstResult)
                nUserTypeID     =   lstResult[0]['nUserTypeID']
            
        if not lstResult:

            return Response(
                                {
                                    "status"    :   False,
                                    "message"   :   "Phone number not found",
                                    "Response"  :   []
                                },
                                    status=status.HTTP_200_OK
                            )
        dtResponseList      =   []
        
        for dtRow in lstResult:

            if not isinstance(dtRow, dict):
                print("Unexpected row:", repr(dtRow), type(dtRow))
                continue

            if  nUserTypeID     ==  1:
                nUserID         =   dtRow.get('nUserMaterID', 0)
                cName           =   dtRow.get('cFullName', 0)
             
            elif nUserTypeID    ==  2:
                nUserID         =   dtRow.get('nUserMaterID', 0)
                cName      =   dtRow.get('cFullName', 0) 
               
            else:
                nUserID         =   0           # dtRow.get('nFamilyMemberID', 0)
               
                cName           =   'Guest Guest'

            dtResponseList.append(
                                    {
                                        'nUserID'               :   nUserID,
                                        'Full Name'             :   cName,
                                        'nUserTypeID'           :   nUserTypeID
                                    
                                    }
                                )

        return Response(
                            {
                                'Response'   :   dtResponseList   
                            },
                                status  =   status.HTTP_200_OK
                        )

@api_view(['POST'])

def fnVerifyPreviousInstallation(request):

    if request.method       ==  "POST":
        
        szDeviceData        =   DeviceSerializer(data  =   request.data)
        nUserID             =   request.data["nUserID"]     
        nUserTypeID         =   request.data["nUserTypeID"]
        lstResult           =   []

        if not szDeviceData.is_valid():
        
            return Response(
                                {
                                    "status"    :   False,
                                    "errors"    :   szDeviceData.errors
                                },  status=400
            )
        
        lstResult       =   fnVerifyInstallation(       nUserID
                                                    ,   nUserTypeID
                                                   
                                                )

        if not lstResult:

            return Response(
                {
                    "status": False,
                    "message": "Phone number not found",
                    "Response": []
                },
                status=status.HTTP_200_OK
            )        
        
        dtResponseList      =   []
        

        if  len(lstResult)   >   0:

            for dtRow in lstResult:

                if not isinstance(dtRow, dict):
                    print("Unexpected row:", repr(dtRow), type(dtRow))
                    continue

            
            nUserDeviceMasterID     =   dtRow.get('nUserDeviceMasterID', 0)
            nDeviceModelMasterID    =   dtRow.get('nDeviceModelMasterID', 0)
            cManufacturer           =   dtRow.get('cManufacturer', 0) 
            cDeviceModel            =   dtRow.get('cDeviceModel', 0)
 
            dtResponseList.append(
                                    {   'nUserDeviceMasterID'   :   nUserDeviceMasterID,
                                        'nDeviceModelMasterID'  :   nDeviceModelMasterID,
                                        'cManufacturer'         :   cManufacturer,
                                        'cDeviceModel'          :   cDeviceModel,
                                    }
                                )

        return Response(
                            {
                                'Response'   :   dtResponseList   
                            },
                                status  =   status.HTTP_200_OK
                        )

@api_view(['POST'])

def fnAddUser(request):
     if request.method       ==  "POST":
                
                szUserData          =   UserSerializer(data  =   request.data)
                nLanguageID         =   request.data["nLanguageID"]
                cFirstName          =   request.data["cFirstName"]
                cLastName           =   request.data["cLastName"]
                dDoB                =   request.data["dDoB"]
                nGenderID           =   request.data["nGenderID"]
                cAddress            =   request.data["cAddress"]
                cPhoneNumber        =   request.data["cPhoneNumber"]
                nIDTypeID           =   request.data["nIDTypeID"]
                cIDCardNumber       =   request.data["cIDCardNumber"]
                nLat                =   request.data["nLat"]
                nLong               =   request.data["nLong"]
                nUserTypeID         =   int(request.data["nUserTypeID"])
                print(nUserTypeID)
                iMode                   =   request.data["nInstallationType"]
                cProfilePictures        =   request.FILES.get('cProfilePicture') 
                         # the uploaded file
                cProfilePicture     =   fnSaveandUploadImageFile(
                                            cProfilePictures
                                        ,   'User/ProfilePics'
                                        ) or ''

                try:

                    dtUser = fnGetUserByPhoneNumber(cPhoneNumber)
                    print(dtUser,"dtUser")
                    if dtUser:
                        if nUserTypeID == 1:
                                print("hhhhh")

                            
                                return Response(
                                    {
                                        "status"  : False,
                                        "message" : "User already registered with this phone number"
                                    }, status=400
                                )

                        elif nUserTypeID == 2:
                                fnUpdateUserTypeID(
                                                dtUser['nUserMaterID']
                                            ,   2
                                        )

                                lstResult = fnReturnUserDetails(
                                    nUserMaterID=dtUser['nUserMaterID']
                                )
                                return Response(
                                            {
                                                "status"  : True,
                                                "message" : "User type updated successfully",
                                                "data"    : lstResult
                                            }, status=200
                                        )
                except Exception as oError:

                    return Response(
                        {
                            "status"  : False,
                            "message" : str(oError)
                        }, status=400
                    )

                lstResult           =   []

                if not szUserData.is_valid():
                
                    return Response(
                                        {
                                            "status"    :   False,
                                            "errors"    :   szUserData.errors
                                        },  status=400
                    )
                try:
                        nNewUserMaterID =   fnAddUserMasterDetails(     nLanguageID
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
                                                                )
                except Exception as oError:
                     
                        if cProfilePicture:
                            cFilePath = os.path.join(settings.MEDIA_ROOT, 'User', 'ProfilePics', cProfilePicture)
                            if os.path.exists(cFilePath):
                                os.remove(cFilePath)
                        return Response(
                            {
                                "status"    :   False,
                                "message"   :   str(oError)
                            },  status = 400
                        )
                if nNewUserMaterID:
                    lstResult   =   fnReturnUserDetails(nUserMaterID = nNewUserMaterID)

                    return Response(
                                        {
                                            "status"    :   True,
                                            "message"   :   "User added successfully",
                                            "data"      :   lstResult
                                        },  status = 201
                                    )

                return Response(
                                    {
                                        "status"    :   False,
                                        "message"   :   "User could not be added"
                                    },  status = 400
                                )

@api_view(['POST'])

def fnDeviceInstallUpdate(request):
    
    if request.method           ==  "POST":
        
        szDeviceData            =   DeviceSerializer(data  =   request.data)
        szPhoneNo               =   PhoneSerializer(data  =   request.data)

        bPhoneValid  = szPhoneNo.is_valid()
        bDeviceValid = szDeviceData.is_valid()

        if not bPhoneValid or not bDeviceValid:     
        
            return Response(
                                {
                                    "status": False,
                                    "errors": {
                                                "Phone": szPhoneNo.errors,
                                                "Device": szDeviceData.errors
                                            }
                                },
                                status=400
                            )

        cPhoneNumber            =   szPhoneNo.validated_data["cPhoneNumber"]        
        nUserDeviceMasterID     =   request.data["nUserDeviceMasterID"]
        nLanguageID             =   szDeviceData.validated_data["nLanguageID"]
        nDeviceModelMasterID    =   request.data["nDeviceModelMasterID"] 
        cDeviceUUID             =   szDeviceData.validated_data["cDeviceUUID"] 
        nDeviceTypeID           =   szDeviceData.validated_data["nDeviceTypeID"]
        nDeviceModelMasterID    =   request.data["nDeviceModelMasterID"]
        nUserTypeID             =   request.data["nUserTypeID"]
        nUserID                 =   request.data["nUserID"]
        cFCMToken               =   szDeviceData.validated_data["cFCMToken"]
        nLat                    =   szDeviceData.validated_data["nLat"]
        nLong                   =   szDeviceData.validated_data["nLong"]        
        iMode                   =   request.data["nInstallationType"]
 
        bResult     =   fnSaveUserDeviceMasterDetails(      nUserDeviceMasterID     
                                                        ,   nLanguageID
                                                        ,   cPhoneNumber
                                                        ,   cDeviceUUID
                                                        ,   nDeviceTypeID
                                                        ,   nDeviceModelMasterID
                                                        ,   nUserTypeID
                                                        ,   nUserID
                                                       
                                                        ,   cFCMToken
                                                        ,   nLat
                                                        ,   nLong
                                                        ,   iMode
                                                    )
 

        return Response(
                                {   "message": "Added Successfully"   if iMode == 1 
                                    else 
                                    "Updated Successfully"},status=status.HTTP_200_OK
                            )

@api_view(['POST'])
def fnSaveService(request):

    szServiceData   =   ServiceSerializer(data = request.data)

    if not szServiceData.is_valid():
        return Response(
                            {
                                "status"    :   False,
                                "errors"    :   szServiceData.errors
                            },  status = 400
                        )

    data               =   szServiceData.validated_data
    iMode           =   int(request.data.get("iMode", 1))

    if iMode == 2 and int(data['nServiceMssterID']) <= 0:
        return Response(
                            {
                                "status"    :   False,
                                "message"   :   "nServiceMssterID is required for update"
                            },  status = 400
                        )

    # save the uploaded images, keep only the file names
    lstImages       =   []

    for oFile in data['cImages']:
        cFileName   =   fnSaveandUploadImageFile(oFile, 'Service/Images')
        if cFileName:
            lstImages.append(cFileName)

    try:
        nServiceMasterID    =   fnSaveServiceMasterDetails(
                                        data['nServiceMasterID']
                                    ,   data['nOrganizationID']
                                    ,   data['nBranchID']
                                    ,   data['nDepartmentID']
                                    ,   data['nCategoryID']
                                    ,   data['cServiceName']
                                    ,   data['cBrand']
                                    ,   data['cModelNo']
                                    ,   data['dManufacturingDate']
                                    ,   data['dWorkStartTime']
                                    ,   data['dWorkEndTime']
                                    ,   data['nOperationRangeYN']
                                    ,   data['nOperationRangeKms']
                                    ,   data['nStaffNeededYN']
                                    ,   data['nHolidayIncludedYN']
                                    ,   ''
                                    ,   data['cDescriptions']
                                    ,   lstImages
                                    ,   iMode
                                )
        print(nServiceMasterID,"nServiceMasterID")
    except Exception as oError:
        # the database rolled back, so remove the files that were just saved
        for cFileName in lstImages:
            cFilePath   =   os.path.join(settings.MEDIA_ROOT, 'Service', 'Images', cFileName)
            if os.path.exists(cFilePath):
                os.remove(cFilePath)

        return Response(
                            {
                                "status"    :   False,
                                "message"   :   str(oError)
                            },  status = 400
                        )

    return Response(
                        {
                            "status"            :   True
                        ,   "message"           :   "Service saved successfully"
                        ,   "nServiceMasterID"  :   nServiceMasterID
                        },  status = 201 if iMode == 1 else 200
                    )