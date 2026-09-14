from rest_framework import serializers
from .models import CarMake, CarModel

class CarMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMake
        fields = ['id', 'name', 'slug', 'icon']

class CarModelSerializer(serializers.ModelSerializer):
    make = CarMakeSerializer(read_only=True)
    make_id = serializers.PrimaryKeyRelatedField(
        queryset=CarMake.objects.all(),
        write_only=True,
        source='make'
    )

    class Meta:
        model = CarModel
        fields = [
            'id', 'name', 'make', 'make_id', 'year_start', 'year_end',
            'slug', 'icon'
        ] 