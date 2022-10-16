from rest_framework import serializers


class GoodsSerializer(serializers.Serializer):
    article = serializers.IntegerField(read_only=False)
    title = serializers.CharField(read_only=True)
    brand = serializers.CharField(read_only=True)
    file = serializers.FileField(write_only=True)

