from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import user_collection
import re
import logging

logger = logging.getLogger(__name__)
class SearchUserView(APIView):
    def post(self, request):
        try:
            search_query = request.data["search"]
            logger.info("Received search query: %s", search_query)

            # remove leading/trailing whitespaces 
            search_query = search_query.strip()
            logger.debug("Trimmed search query: %s", search_query)
            
            # if no search query is provided will throw an error
            if len(search_query) == 0:
                logger.warning("Empty search query provided.")
                return Response({"error": "please provide a valid user name"}, status=400)
            
            tokens = search_query.split()
            logger.debug("Search tokens: %s", tokens)
            
            if len(tokens) == 1:
                # if we have single token, will search both first_name and last_name using OR
                token = re.escape(tokens[0])
                logger.debug("Single token detected: %s", token)
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
                logger.debug("Multiple tokens detected - first: %s, last: %s", first, last)
                query = {
                    "first_name": {"$regex": f"^{first}", "$options": "i"},
                    "last_name": {"$regex": f"^{last}", "$options": "i"}
                }

            logger.info("MongoDB query constructed: %s", query)
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
            logger.info("Number of users found: %d", len(result))
            
            message = "successfully fetched users list"
            statusCode = status.HTTP_200_OK

            if len(result) == 0:
                message = "No user found with the given search"
                statusCode = status.HTTP_400_BAD_REQUEST
                logger.info("No users found for query: %s", search_query)
            return Response({
                "data":result,
                "message":message
            },
            status=statusCode
            )
        except Exception as e:
            logger.exception("Exception occurred in search_user view: %s", e)
            return Response({
                "data":[],
                "message":"Something went wrong"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


