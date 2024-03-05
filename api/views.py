import uuid
from datetime import datetime

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .utility import uni_validation

from .models import NewsStory, User, Agency
from .serializers import UserSerializer, NewsStorySerializer, AgencySerializer


class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            if uni_validation(request):
                user = authenticate(request, username=username, password=password)
                if user:
                    token, created = Token.objects.get_or_create(user=user)

                    return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
                else:
                    return Response('Invalid credentials', status=status.HTTP_503_SERVICE_UNAVAILABLE)
            else:
                return Response('Domain not found', status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({'error: ': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            if uni_validation(request):
                Token.objects.get(user=request.user).delete()
                return Response({'message': 'Successfully Logout'}, status=status.HTTP_200_OK)
            else:
                return Response('Domain not found', status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)


class NewsStoryView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = NewsStory.objects.all()
    serializer_class = NewsStorySerializer

    def post(self, request, *args, **kwargs):
        if uni_validation(request):
            unique_key = f'{uuid.uuid4().hex}_{int(datetime.utcnow().timestamp())}'
            truncated_key = unique_key[:20]
            key = truncated_key
            request.data['key'] = key
            request.data['author'] = request.user.id
            serializer = NewsStorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(f'Domain not found', status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def get(self, request, *args, **kwargs):
        story_cat = self.request.data.get('story_cat')
        story_region = self.request.data.get('story_region')
        story_date = self.request.data.get('story_date')

        queryset = NewsStory.objects.filter(
            category=story_cat,
            region=story_region,
            date=story_date
        )
        serializer = NewsStorySerializer(queryset, many=True)
        return Response({"stories": serializer.data}, status=status.HTTP_200_OK)


class NewsStoryDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = NewsStory.objects.all()
    serializer_class = NewsStorySerializer

    def destroy(self, request, *args, **kwargs):
        if uni_validation(request):
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response("NewsStory deleted successfully.", status=status.HTTP_204_NO_CONTENT)
        return Response(f'Domain not found', status=status.HTTP_503_SERVICE_UNAVAILABLE)


class DirectoryAPIView(ListCreateAPIView):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer

    def create(self, request, *args, **kwargs):
        try:
            request.data['agency_code'] = request.data.get('agency_code').lower()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response('Request processed successfully', status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "agency_list": serializer.data
        }
        return Response(data)
