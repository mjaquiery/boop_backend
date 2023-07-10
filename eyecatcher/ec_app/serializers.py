import base64
from hashlib import md5
from json import JSONDecodeError

from django.core.files.base import ContentFile

from .models import System, Report
from rest_framework import serializers


class SystemSerializer(serializers.HyperlinkedModelSerializer):
    auth_code = serializers.CharField(write_only=True)

    class Meta:
        model = System
        fields = ['url', 'id', 'properties', 'reports', 'auth_code']
        extra_kwargs = {
            'reports': {'read_only': True},
        }


class CreateSystemSerializer(serializers.HyperlinkedModelSerializer):
    auth_code = serializers.SerializerMethodField(read_only=True)

    def get_auth_code(self, obj):
        return obj.get_auth_code(obj.properties)

    class Meta:
        model = System
        fields = ['url', 'id', 'properties', 'reports', 'auth_code']
        extra_kwargs = {
            'reports': {'read_only': True},
        }


class ImageField(serializers.CharField):
    def to_representation(self, value):
        with open(value.path, mode='rb') as file:  # b is important -> binary
            content = file.read()
            encoded_base64 = base64.b64encode(content)  # return bytes
            return encoded_base64.decode('utf-8')

    def to_internal_value(self, data):
        fmt, img_str = data.split(';base64,')
        ext = fmt.split('/')[-1]

        data = ContentFile(
            base64.b64decode(img_str),
            name=f"{md5(img_str.encode('utf-8')).hexdigest()}.{ext}"
        )
        return data


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    auth_code = serializers.CharField(write_only=True, required=True)
    system_properties = serializers.JSONField(write_only=True, required=True)
    image = ImageField(required=True)
    time_created = serializers.DateTimeField(read_only=True)

    def validate(self, data):
        try:
            if not data["system"].verify_auth_code(data['auth_code'], data['system_properties']):
                raise serializers.ValidationError("Invalid auth code")
        except (KeyError, System.DoesNotExist, JSONDecodeError) as e:
            raise serializers.ValidationError(f"Error validating auth code: {e}")
        data.pop('auth_code')
        data.pop('system_properties')
        return data

    class Meta:
        model = Report
        fields = ['url', 'id', 'time_created', 'system', 'click_data', 'image', 'system_properties', 'auth_code']
