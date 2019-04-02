from rest_framework import serializers
from url_app.models import Url


class UrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Url
        fields = ('url', 'title', 'short_url', 'clicks', 'create_dttm')
