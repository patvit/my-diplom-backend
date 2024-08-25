from rest_framework import serializers

from .models import Document
from accounts.models import CustomUser


class DocumentSerializer(serializers.ModelSerializer):
    filename = serializers.CharField(max_length=255, default='')
    description = serializers.CharField(max_length=255, default='')
    upload_datetime = serializers.SerializerMethodField()
    uploaded_by = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    size = serializers.SerializerMethodField()
    share_link = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ('id', 'filename', 'file', 'description',
                  'upload_datetime', 'uploaded_by', 'size', 'share_link')

    def get_upload_datetime(self, obj):
        return obj.upload_datetime

    def get_size(self, obj):
        return obj.size

    def get_share_link(self, obj):
        return obj.share_link

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        uploaded_by_id = representation['uploaded_by']
        user = CustomUser.objects.filter(pk=uploaded_by_id).values(
            'username').first() if uploaded_by_id else None
        representation['uploaded_by'] = user['username'] if user else None

        return representation
