from rest_framework import serializers
from .fields         import (       PhoneNumberField
                                ,   DeviceUUIDField
                                ,   nLatitude
                                ,   nLongitude
                            )   
from datetime import date

class OrganizationSerializer(serializers.Serializer):
    nCountryID=serializers.IntegerField()
    nStateID=serializers.IntegerField()
    nDistrictID=serializers.IntegerField()
    nDioceseID=serializers.IntegerField()
    nForaneID=serializers.IntegerField()
    nParishID=serializers.IntegerField()
    nPradeshikamID=serializers.IntegerField()
    nWardID=serializers.IntegerField()
    nFamilyUnitID=serializers.IntegerField()


class   PhoneSerializer(serializers.Serializer):
    cPhoneNumber        =   PhoneNumberField(required   =   True)


class   DeviceSerializer(serializers.Serializer):

    cPhoneNumber        =   PhoneNumberField(required   =   True)
    cDeviceUUID         =   DeviceUUIDField(required=False, allow_null=True,allow_blank=True)
    nLanguageID         =   serializers.IntegerField(required   =   True)
    cFCMToken           =   serializers.CharField(max_length=512)
    nDeviceTypeID       =   serializers.IntegerField()
    cDeviceModel        =   serializers.CharField()
    cManufacturer       =   serializers.CharField()
    cOSVersion          =   serializers.CharField()
    cSDKVersion         =   serializers.CharField()
    # nLat                =   nLatitude(required=False)
    # nLong               =   nLongitude(required=False)





class   UserSerializer(serializers.Serializer):

    nLanguageID         =   serializers.IntegerField(min_value=1)
    cFirstName          =   serializers.CharField(max_length=50)
    cLastName           =   serializers.CharField(max_length=100)
    dDoB                =   serializers.DateField()
    nGenderID           =   serializers.ChoiceField(choices=[1, 2, 3])   # 1 = Male, 2 = Female, 3 = Other
    cAddress            =   serializers.CharField(max_length=500)
    cPhoneNumber        =   PhoneNumberField(required   =   True)
    nIDTypeID           =   serializers.IntegerField(min_value=1)
    cIDCardNumber       =   serializers.CharField(max_length=25)
    nLat                =   nLatitude(required=False)
    nLong               =   nLongitude(required=False)
    cProfilePicture     =   serializers.FileField(max_length=500)
    nUserTypeID         =   serializers.IntegerField(min_value=0, max_value=255)   # TINYINT

    def validate_dDoB(self, value):
        if value >= date.today():
            raise serializers.ValidationError("Date of birth must be in the past.")
        return value


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