from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class StudyPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    typeOfStudy = models.CharField(max_length=30)
    wantChazara = models.IntegerField()


class DafLearning1(models.Model):
    # indexTypeOfStudy = models.IntegerField()
    masechet = models.TextField(max_length=50 )
    pageNumber = models.IntegerField()
    isLearning = models.BooleanField(default=False)
    chazara = models.IntegerField()
    # isLearningPage1 = models.BooleanField()
    # isLearningPage2 = models.BooleanField()
    typeOfStudy = models.ForeignKey(StudyPlan, on_delete=models.CASCADE)
    pageDate = models.TextField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

