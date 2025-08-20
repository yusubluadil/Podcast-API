from rest_framework import serializers


class ExternalUrlsSerializer(serializers.Serializer):
    spotify = serializers.CharField(allow_blank=True, required=False)


class ImageSerializer(serializers.Serializer):
    url = serializers.CharField()
    height = serializers.IntegerField(allow_null=True, required=False)
    width = serializers.IntegerField(allow_null=True, required=False)


class ShowSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    publisher = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)
    languages = serializers.ListField(child=serializers.CharField(), required=False)
    media_type = serializers.CharField(required=False)
    total_episodes = serializers.IntegerField(required=False)
    images = ImageSerializer(many=True, required=False)
    external_urls = ExternalUrlsSerializer(required=False)
    available_markets = serializers.ListField(child=serializers.CharField(), required=False)


class EpisodeSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(allow_blank=True, required=False)
    release_date = serializers.CharField(required=False)
    duration_ms = serializers.IntegerField(required=False)
    explicit = serializers.BooleanField(required=False)
    audio_preview_url = serializers.CharField(allow_null=True, required=False)
    images = ImageSerializer(many=True, required=False)
    external_urls = ExternalUrlsSerializer(required=False)
    languages = serializers.ListField(child=serializers.CharField(), required=False)
