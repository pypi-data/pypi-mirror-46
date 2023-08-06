from rest_framework import serializers

from rebotics_sdk.notifications.models import WebhookRouter


class SetWebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookRouter
        fields = [
            'url',
        ]
