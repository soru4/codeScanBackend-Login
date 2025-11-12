from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),



    # Include your users application URLs (for registration, profile, etc.)
    path('api/users/', include('users.urls')),
]