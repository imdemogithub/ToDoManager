from django.urls import path
from .views import *

urlpatterns = [
    path('', login_page),
    path('register_page/', register_page, name="register_page"),
    path('recovery_password_page/', recovery_password_page, name="recovery_password_page"),
    path('profile_page/', profile_page, name="profile_page"),
    path('register/', register, name="register"),
    path('login/', login, name="login"),
    path('sign_out/', sign_out, name="sign_out"),
    path('profile_update/', profile_update, name="profile_update"),
    path('change_password/', change_password, name="change_password"),
    path('search_ref/', search_ref, name="search_ref"),
    path('create_todo/', create_todo, name="create_todo"),
    path('remove_todo/<int:pk>/', remove_todo, name="remove_todo"),
    path('upload_image/', upload_image, name="upload_image"),
]