from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer

class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data['data'], many=True)
        if serializer.is_valid():
            serializer.save()  # Saves user data to DB
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        users = User.objects.all()  # Retrieve all users
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    