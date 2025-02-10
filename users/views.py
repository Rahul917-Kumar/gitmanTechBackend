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



class SearchUserView(APIView):
    def post(self, request):
        try:
            query = request.data["search"]
            print("query", request.data["search"])
            if len(query) == 0:
                return Response({"error": "Name parameter is required"}, status=400)
            
            users = User.objects.filter(first_name__istartswith=query)
            serializer = UserSerializer(users, many=True)
            user_list = serializer.data
            
            message = "successfully fetched users list"
            statusCode = status.HTTP_200_OK

            if len(user_list) == 0:
                message = "No user found with the given search"
                statusCode = status.HTTP_400_BAD_REQUEST
            return Response({
                "data":user_list,
                "message":message
            },
            status=statusCode
            )
        except:
            return Response({
                "data":user_list,
                "message":message
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )