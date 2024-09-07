from rest_framework import serializers
from .models import *

# Create your serializers here.

class AddPackSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPackage
        fields = ['name','description','author','category','image','video','price_with_discount']
