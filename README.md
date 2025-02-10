# Description
In this project i worked on an API to get list of user from MONGODB which mathces the search query provided by the user.<br></br>
This API endpoint is designed to perform a user search in a MongoDB database based on a provided search query. It is built using Django REST Framework (DRF) and PyMongo. The main goal is to allow clients to search for users by their names in a flexible, case-insensitive manner—whether the search input is a partial first name, a full name (first and last), or just a surname.

### Details about the API?
Scoring Logic for Matching Users

For every user document, the API computes a matching score based on several criteria:

    Exact Match:
        If the search query exactly matches the user's first_name or last_name, a high score (5 points) is given.

    Exact Full Name Match:
        If the query exactly equals the normalized full name (concatenation of first and last names with spaces removed), 5 points are added.

    Prefix Matching:
        If the normalized first_name starts with the query, it gets 4 points.
        If the normalized last_name starts with the query, it also gets 4 points.

    This ensures that if the query is a prefix (like "amit") of either field, the user is considered a strong match.

    Flexible Spacing:
        If the normalized query (with spaces removed) equals the normalized full name, the user is awarded 4 points.
        This allows a search like "amitsharma" to potentially match "amit sharma" even if the user didn’t include the space.

    Handling Two-Word Queries:
        If the query consists of exactly two words, the algorithm checks if:
            The first word matches the start of the first_name and the second word matches the start of the last_name (score: 5 points).
            If only one of these conditions is met, a partial score of 4 is assigned.
            If the words appear swapped (for example, "KD Rahul" instead of "Rahul KD"), a slightly lower score of 3 is given.

    This scoring gives preference to the correct order (first name first, last name second) while still allowing for some flexibility.

## Example
endpoint ``` /users/search-user/ ```

![image](https://github.com/user-attachments/assets/18188863-d4e8-4d30-a265-057fe40e9a2f)
