from .models import DafLearning1
from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    # path('daflearning', views.DafLearning1List.as_view(), name="daflearning_list"),
    # path('daflearning/<int:pk>', views.DafLearning1Detail.as_view(), name="daflearning_detail"),
    path('studyplan', views.StudyPlanViews.as_view(), name="studyplan_detail"),
    path('studyplan/<type>', views.StudyPlanViews.as_view(), name="studyplan_detail"),
    path('daflearning', views.DafLearningViews.as_view(), name='daflearning'),
    path('daflearning/<type>', views.DafLearningViews.as_view())
]