import      phonenumbers
from        rest_framework import serializers
import      uuid


class PhoneNumberField(serializers.CharField):

    def to_internal_value(self, data):

        value = super().to_internal_value(data).strip()

        try:
            phone = phonenumbers.parse(value, None)

        except phonenumbers.NumberParseException:
            raise serializers.ValidationError(
                                                "Enter a valid Phone Number."
                                            )

        if not phonenumbers.is_valid_number(phone):
            raise serializers.ValidationError(
                                                "Enter a valid Phone Number."
                                            )

        return phonenumbers.format_number(
                                            phone,
                                            phonenumbers.PhoneNumberFormat.E164
                                        )

class DeviceUUIDField(serializers.CharField):
    
    def to_internal_value(self, data):

        if data is None:
            return None

        cUUID = str(data).strip()

        if cUUID.lower() in ("", "null"):
            return None

        try:
            return str(uuid.UUID(str(cUUID)))
        except (ValueError, AttributeError, TypeError):
            raise serializers.ValidationError(
                "Must be null or a valid UUID."
            )

class nLatitude(serializers.DecimalField):

    def __init__(self, **kwargs):
        super().__init__(
            max_digits=10,
            decimal_places=7,
            **kwargs
        )

    def fnValidateLat(self, nLatitude):
        nLat = super().validate(nLatitude)

        if nLat < -90 or nLat > 90:
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90."
            )
        return nLat

class nLongitude(serializers.DecimalField):

    def __init__(self, **kwargs):
        super().__init__(
            max_digits=11,
            decimal_places=7,
            **kwargs
        )

    def fnValidateLat(self, nLongitude):
        nLong = super().validate(nLongitude)

        if nLong < -180 or nLong > 180:
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90."
            )
        return nLong