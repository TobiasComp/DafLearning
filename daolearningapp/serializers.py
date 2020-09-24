from rest_framework import serializers
from .models import DafLearning1, StudyPlan

class DafLearning1Serializer(serializers.ModelSerializer):
    class Meta:
        model = DafLearning1
        fields = ['id', 'masechet', 'pageNumber',
                  'isLearning', 'chazara',
                  'typeOfStudy', 'pageDate', 'typeOfStudy__typeOfStudy']


class StudyPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyPlan