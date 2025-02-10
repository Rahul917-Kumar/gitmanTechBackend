# Description
In this project i worked on an API to get list of user from MONGODB which mathces the search query provided by the user.<br></br>
This API endpoint is designed to perform a user search in a MongoDB database based on a provided search query. It is built using Django REST Framework (DRF) and PyMongo. The main goal is to allow clients to search for users by their names in a flexible, case-insensitive manner—whether the search input is a partial first name, a full name (first and last), or just a surname.

### Details about the API?
Depending on the input:<br></br>

  <b>Single Token Input</b>:<br></br>
    If the search query consists of only one word (e.g., "am"), the API searches for any user whose first name or last name starts with that token. This is done using an OR condition in the database query.<br></br>
##### Example
so it will search both first_name and last_name for a user and use or operator that either of the two condition should match
```
{
    "search":"am"
}
```

![image](https://github.com/user-attachments/assets/817c34cc-baba-4055-a147-b66bc56d1b4a)

```
{
    "search":"sh"
}
```
![image](https://github.com/user-attachments/assets/b3ddd6b4-235e-49f0-bbb2-77e68e8c603b)
  <b>Multiple Token Input</b>:<br></br>
    If the search query contains multiple words (e.g., "Amit Sharma"), the API assumes that the first token corresponds to the first_name and the last token corresponds to the last_name. It then builds a query that requires both fields to start with the respective tokens, resulting in a more refined search.
##### Example
so the algorithm compares first token to first_name and second token to last_name and take and of it

![image](https://github.com/user-attachments/assets/5dafc49c-c92c-4e10-ab56-a0564a8d8229)
