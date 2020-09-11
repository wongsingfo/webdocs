from django.contrib.auth.models import User
from rest_framework import serializers

from page.models import Document, Image

class UserConciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class DocumentSerializer(serializers.ModelSerializer):
    owner = UserConciseSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'title', 'owner', 'abstract', 'body', 'created', 'last_modified']
        read_only_fields = ['created', 'last_modified']

    @classmethod
    def many_init(cls, *args, **kwargs):
        allow_empty = kwargs.pop('allow_empty', None)
        child_serializer = cls(*args, **kwargs)
        # Don't show body when retrieving multiple documents
        child_serializer.fields.pop('body')
        list_kwargs = {
            'child': child_serializer,
        }
        if allow_empty is not None:
            list_kwargs['allow_empty'] = allow_empty
        list_kwargs.update({
            key: value for key, value in kwargs.items()
            if key in serializers.LIST_SERIALIZER_KWARGS
        })
        meta = getattr(cls, 'Meta', None)
        list_serializer_class = getattr(meta, 'list_serializer_class', serializers.ListSerializer)
        return list_serializer_class(*args, **list_kwargs)


class UserSerializer(serializers.ModelSerializer):
    documents = serializers.HyperlinkedRelatedField(
        many=True, view_name='document-detail', read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'documents']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image', 'document']
