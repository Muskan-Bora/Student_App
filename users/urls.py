from django.urls import path, include
from users import views as userviews

app_name = 'users'

urlpatterns = [
    # Register/Sign Up Page -----------------------
    path('register/', userviews.register, name='register'),

    # Login Page ------------------------------------
    path('login/', userviews.login_view, name='login'),

    # Logout Page --------------------------------------
    path('logout/', userviews.logout_view, name='logout'),

    path('profile/', userviews.profile_page, name='profile'),
    path('profile/profform/', userviews.profform, name='profform'),
]