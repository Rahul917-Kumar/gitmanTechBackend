
from django.urls import path
from .views import SearchUserView

urlpatterns = [
    path('search-user/', SearchUserView.as_view(), name='search_user'),
]
