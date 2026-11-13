from django.shortcuts import render
from rest_framework.decorators              import  api_view
from rest_framework.response                import  Response
from glossmeapp.serializers                 import  *
from rest_framework                         import  status
from CommonDetails.CommonDetailFunctions    import *

# Create your views here.
@api_view(['GET','POST'])
def fnGetBrands(request):
    if request.method == 'POST':
        cBrandName = (request.data.get('cBrandName') or '').strip()
        lstResult = fnGetBrandList(cBrandName=cBrandName) or []
    else:
   

        lstResult = fnGetBrandList() or []

    return Response({'nResult': 1, 'data': lstResult})