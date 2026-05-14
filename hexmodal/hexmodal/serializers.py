import base64

from django.db import transaction
from rest_framework import serializers

from hexmodal.models import Payload, Device, StatusChoices


class PayloadSerializer(serializers.ModelSerializer):
    rxInfo = serializers.JSONField(write_only=True, required=False)
    txInfo = serializers.JSONField(write_only=True, required=False)
    devEUI = serializers.CharField(write_only=True)

    class Meta:
        model = Payload
        fields = ['id', 'fCnt', 'data', 'rxInfo', 'txInfo', 'devEUI']

    def validate(self, attrs):
        # Ensure this payload is not a duplicate
        if Payload.objects.filter(fCnt=attrs.get('fCnt')).exists():
            raise serializers.ValidationError('Duplicate payload')

        # Parse Base64 value to hexadecimal and set status
        base64_raw = attrs.get('data')
        decoded_data = base64.b64decode(base64_raw)

        try:
            decoded_data = int.from_bytes(decoded_data, byteorder='big')
        except ValueError:
            decoded_data = 0

        if decoded_data == 1:
            attrs['status'] = StatusChoices.PASSING
        else:
            attrs['status'] = StatusChoices.FAILING

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        device_id = validated_data.get('devEUI')

        # TODO: Clarify missing device behaviour, for now we create it
        device, _ = Device.objects.get_or_create(devEUI=device_id)
        device.latest_status = validated_data.get('status')
        device.save(update_fields=['latest_status'])

        validated_data.pop('devEUI')
        validated_data.pop('rxInfo', None)
        validated_data.pop('txInfo', None)

        return Payload.objects.create(
            device=device, **validated_data
        )
