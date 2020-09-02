from django.contrib.auth.models import User
from rest_framework import serializers

from page.models import Document, Image


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Document
        fields = ['url', 'id', 'title', 'owner', 'body', 'created', 'last_modified']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    documents = serializers.HyperlinkedRelatedField(
        many=True, view_name='document-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff', 'documents']


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ['url', 'image', 'document']
