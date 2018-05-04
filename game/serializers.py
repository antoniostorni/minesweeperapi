from rest_framework import serializers
from .models import Grid, Square

class GridSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grid
        fields = '__all__'


class SquareSerializer(serializers.ModelSerializer):

    class Meta:
        model = Square
        fields = '__all__'
