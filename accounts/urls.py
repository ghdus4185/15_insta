from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('<int:id>/', views.user_page, name="user_page"),
    path('<int:id>/follow/', views.follow, name="follow"),
]
