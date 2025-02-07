
from django.urls import path
from .views import UserCreateView, SearchUserView

urlpatterns = [
    path('user/', UserCreateView.as_view(), name='store_get_user'),
    path('search-user/', SearchUserView.as_view(), name='search_user'),

]
