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


