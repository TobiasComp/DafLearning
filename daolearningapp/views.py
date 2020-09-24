from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.forms import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_201_CREATED

from .models import DafLearning1, StudyPlan
from .serializers import DafLearning1Serializer, StudyPlanSerializer
from rest_framework import generics



class StudyPlanViews(generics.GenericAPIView):
    serializer_class = StudyPlanSerializer

    def post(self, request):
        user = request.user
        want_chazara = request.data.get('want_chazara')
        type_of_study = request.data.get('type_of_study')
        StudyPlan.objects.create(user=user, typeOfStudy=type_of_study, wantChazara=want_chazara)
        return Response(data={'message': 'study plan created'}, status=HTTP_201_CREATED)

class DafLearningViews(generics.GenericAPIView):
    def get(self, request, **kwargs):
        type = self.kwargs.get('type')
        user = request.user
        type_of_study = StudyPlan.objects.get(user=user, typeOfStudy=type)
        dafim = DafLearning1.objects.filter(user=user, typeOfStudy=type_of_study).values(
            'id', 'masechet', 'pageNumber', 'isLearning', 'chazara', 'typeOfStudy__typeOfStudy'
        )
        serializer = DafLearning1Serializer(dafim, many=True)
        return JsonResponse(serializer.data, safe=False)
        # return Response(dafim)

    def post(self, request):
        user = request.user
        type_of_study = request.data.get('type_of_study')
        daf = request.data.get('daf')
        masechet = request.data.get('masechet')
        type_of_study = StudyPlan.objects.get(user=user, typeOfStudy=type_of_study)
        if DafLearning1.objects.filter(user=user, typeOfStudy=type_of_study, pageNumber=daf, masechet=masechet).count() > 0:
            old_daf = DafLearning1.objects.get(typeOfStudy=type_of_study, pageNumber=daf, masechet=masechet)
            old_daf.chazara += 1
            old_daf.save()
        else:
            DafLearning1.objects.create(user=user, typeOfStudy=type_of_study, pageNumber=daf, masechet=masechet,
                    isLearning=True, chazara=0, pageDate='')
        return Response(data={'message': 'a daf was learned.'}, status=HTTP_201_CREATED)




@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    try:
        validate_email(email)
    except forms.ValidationError:
        return Response({'error': 'Please provide a valid email address'},
                        status=HTTP_400_BAD_REQUEST)
    if username is None or password is None or email is None:
        return Response({'error': 'Please provide username, password, and email'},
                        status=HTTP_400_BAD_REQUEST)

    if len(User.objects.filter(email=email)) != 0:
        return Response({'error': 'This email address is already taken'},
                        status=HTTP_400_BAD_REQUEST)

    try:
        User.objects.get(username=username)
        return Response({'error': 'This username is already taken'},
                        status=HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password=password, email=email)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)

@csrf_exempt
@api_view(["GET"])
def logout(request):
    token = request.auth
    Token.objects.get(key=token).delete()
    return Response(status=HTTP_200_OK)
