from rest_framework import serializers


class WebhookSerializer(serializers.Serializer):
    """
    Serializer for incoming webhook data.

    Placeholder that should be updated with the actual webhook payload
    structure expected to receive from the webhooks.
    """
    event_type = serializers.CharField(required=True)
    payload = serializers.JSONField(required=True)
    timestamp = serializers.DateTimeField(required=False)

    def validate_event_type(self, value):
        """
        Validate that the event type is one we can handle
        """
        valid_events = ['message.created', 'message.updated',
                        'conversation.created']
        if value not in valid_events:
            raise serializers.ValidationError(
                f"Unsupported event type. Must be one of: {', '.join(valid_events)}")
        return value
