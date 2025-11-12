from django.urls import path
from .views import login_view, currentUser, emailVerification, leave, register,resetPass,sendEmail

urlpatterns = [
    path('login/', login_view, name="login"),
    path('currUser/', currentUser, name="currentUser"),
    path('emailCheck/', emailVerification, name="emailVerification"),
    path('logout/', leave, name="logout"),
    path('register/', register, name="register"),
    path('resetPassword/', resetPass, name="resetPass"),
    path('checkEmail/', sendEmail, name="sendEmail"),
]