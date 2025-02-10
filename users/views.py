from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import user_collection
import re

class SearchUserView(APIView):
    def post(self, request):
        try:
            search_query = request.data["search"]

            # remove leading/trailing whitespaces 
            search_query = search_query.strip()
            
            # if no search query is provided will throw an error
            if len(search_query) == 0:
                return Response({"error": "please provide a valid user name"}, status=400)
            
            tokens = search_query.split()
            
            if len(tokens) == 1:
                # if we have single token, will search both first_name and last_name using OR
                token = re.escape(tokens[0])
                query = {
                    "$or": [
                        {"first_name": {"$regex": f"^{token}", "$options": "i"}},
                        {"last_name": {"$regex": f"^{token}", "$options": "i"}}
                    ]
                }
            else:
                # For multiple tokens, assume the first is first_name and the last is last_name.
                first = re.escape(tokens[0])
                last = re.escape(tokens[-1])
                query = {
                    "first_name": {"$regex": f"^{first}", "$options": "i"},
                    "last_name": {"$regex": f"^{last}", "$options": "i"}
                }

            users_obj_list = user_collection.find(query)

            result = []
            for user in users_obj_list:
                result.append({
                    "id": str(user.get("_id", "")),
                    "first_name": user.get("first_name", ""),
                    "last_name": user.get("last_name", ""),
                    "city": user.get("city", ""),
                    "contact_number": user.get("contact_number", "")
                })
            
            message = "successfully fetched users list"
            statusCode = status.HTTP_200_OK

            if len(result) == 0:
                message = "No user found with the given search"
                statusCode = status.HTTP_400_BAD_REQUEST
            return Response({
                "data":result,
                "message":message
            },
            status=statusCode
            )
        except:
            return Response({
                "data":[],
                "message":"Something went wrong"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


