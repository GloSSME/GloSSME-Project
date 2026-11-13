from rest_framework import serializers
from glossmeapp.fields         import (       PhoneNumberField
                                ,   DeviceUUIDField
                                ,   nLatitude
                                ,   nLongitude
                            )   
from datetime import date

class ServiceSerializer(serializers.Serializer):

    nServiceMasterID        =   serializers.IntegerField(required=False, default=0)
    nOrganizationID         =   serializers.IntegerField(min_value=1)
    nBranchID               =   serializers.IntegerField(min_value=1)
    nDepartmentID           =   serializers.IntegerField(min_value=1)
    nCategoryID             =   serializers.IntegerField(min_value=1)
    cServiceName            =   serializers.CharField(max_length=200)
    cBrand                  =   serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    cModelNo                =   serializers.CharField(max_length=100, required=False, allow_blank=True, default='')
    dManufacturingDate      =   serializers.DateField(required=False, allow_null=True, default=None)
    dWorkStartTime          =   serializers.TimeField()
    dWorkEndTime            =   serializers.TimeField()
    nOperationRangeYN       =   serializers.ChoiceField(choices=[0, 1], default=0)
    nOperationRangeKms      =   serializers.IntegerField(min_value=0, default=0)
    nStaffNeededYN          =   serializers.ChoiceField(choices=[0, 1], default=0)
    nHolidayIncludedYN      =   serializers.ChoiceField(choices=[0, 1], default=0)
    cQRCode                 =   serializers.ImageField(required=False, allow_null=True, default=None)
    nLat                    =   nLatitude(required=False)
    nLong                   =   nLongitude(required=False)
    cDescriptions           =   serializers.ListField(
                                    child       =   serializers.CharField(max_length=500)
                                ,   required    =   False
                                ,   default     =   list
                                )
    cImages                 =   serializers.ListField(
                                    child       =   serializers.ImageField()
                                ,   required    =   False
                                ,   max_length  =   5
                                ,   default     =   list
                                )

    def validate_dManufacturingDate(self, value):
        if value and value > date.today():
            raise serializers.ValidationError("Manufacturing Date Cannot Be In Future.")
        return value

    def validate_cImages(self, value):
        for oFile in value:
            if oFile.size > 1024 * 1024:
                raise serializers.ValidationError(f"{oFile.name} is larger than 1 MB.")
        return value

    def validate(self, data):
        if data['dWorkEndTime'] <= data['dWorkStartTime']:
            raise serializers.ValidationError("Working End Time Must Be After The Start Time.")

        if int(data['nOperationRangeYN']) == 1 and data['nOperationRangeKms'] <= 0:
            raise serializers.ValidationError("Enter The Operation Range In Kms.")

        return data
    def validate_cQRCode(self, value):
        if value and value.size > 1024 * 1024:
            raise serializers.ValidationError("QR Code image is larger than 1 MB.")
        return value