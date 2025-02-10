from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import user_collection
import re

class SearchUserView(APIView):
    
    @staticmethod
    def normalize_name(name):
        """Removes spaces and converts to lowercase for better matching."""
        return re.sub(r'\s+', '', name.lower())
    
    def post(self, request):
        try:
            query = request.data.get("search", "").strip().lower()
            
            if not query:
                return Response({"error": "Query parameter 'search' is required."}, status=400)

            query_parts = query.split()

            users = list(user_collection.find({}, {"first_name": 1, "last_name": 1, "city": 1, "contact_number": 1}))

            results = []
            max_score = 0
            
            for user in users:
                first_name = user.get("first_name", "").strip().lower()
                last_name = user.get("last_name", "").strip().lower()
                full_name = f"{first_name} {last_name}"

                normalized_first_name = self.normalize_name(first_name)
                normalized_last_name = self.normalize_name(last_name)
                normalized_full_name = self.normalize_name(full_name)

                user["id"] = str(user.pop("_id"))

                score = 0

                # Case 1: If query is exactly the first name or last name
                if query == first_name or query == last_name:
                    score += 5
                
                # Case 2: If query matches the normalized full name exactly
                elif query == normalized_full_name:
                    score += 5

                # Case 3: If query is a prefix match of first name or last name
                elif normalized_first_name.startswith(query):
                    score += 4
                elif normalized_last_name.startswith(query):
                    score += 4

                # Case 4: Compare query with full name by removing spacing
                elif self.normalize_name(query) == normalized_full_name:
                    score += 4

                # Case 5: If query has two words, we have to check first and second word separately
                elif len(query_parts) == 2:
                    first_query, second_query = query_parts

                    # Strong match when first word in query matches first word in name
                    if first_name.startswith(first_query) and last_name.startswith(second_query):
                        score += 5
                    elif first_name.startswith(first_query):
                        score += 4
                    elif last_name.startswith(second_query):
                        score += 4

                    # If words are swapped (e.g., "KD Rahul" instead of "Rahul KD")
                    elif last_name.startswith(first_query) and first_name.startswith(second_query):
                        score += 3

                if score > 0:
                    results.append((score, user))
                    max_score = max(max_score, score)

            # return users detail with max score 
            user_result = [user for score, user in results if score == max_score]
            message = "successfully fetched users list"
            statusCode = status.HTTP_200_OK

            if len(user_result) == 0:
                message = "No user found with the given search"
                statusCode = status.HTTP_400_BAD_REQUEST

            return Response({
                "data": user_result,
                "message": message
            }, status=statusCode)

        except Exception as e:
            print("Error in SearchUserView: ", e)
            return Response({
                "data": [],
                "message": "Something went wrong"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
