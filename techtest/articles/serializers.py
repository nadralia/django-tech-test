from rest_framework import serializers

from .models import Article
from techtest.profiles import serializers as ProfileSerializers
from techtest.regions.models import Region


class ArticleSerializer (serializers.ModelSerializer):
    author = ProfileSerializers.ProfileSerializer(read_only=True)

    class Meta:
        model = Article
        fields = (
            "id",
            "title",
            "content",
            "author",
            "created_at",
            "updated_at",

        )
        read_only_fields = (
            'author',
        )

class ArticleRegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ['id', 'code', 'name']