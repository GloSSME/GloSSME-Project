from django.shortcuts import render
from rest_framework.decorators              import  api_view
from rest_framework.response                import  Response
from glossmeapp.serializers                 import  *
from glossme.PublicFunctions                import  *
from rest_framework                         import  status
from ProductDetails.ProductDetailFunctions   import  *
from ProductDetails.serializers             import  *


# Create your views here.
@api_view(['POST'])
def     fnAddProductDetails(request):

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
                                    ,   data['nLat']
                                    ,   data['nLong']
                                    ,   data['cDescriptions']
                                    ,   lstImages
                                    ,   iMode
                                )
        
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