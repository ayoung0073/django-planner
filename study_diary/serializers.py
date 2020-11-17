from .models import Daily, Diary
from rest_framework import serializers

# serializer : models 객체와 querysets 같은 데이터들을 
# JSON, XML과 같은 데이터로 바꿔주는 역할

class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ('date', 'writer', 'title', 'content')
