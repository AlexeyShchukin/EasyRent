from django.urls import path, include

urlpatterns = [
    path('listings/', include('src.listing.urls')),
    path('users/', include('src.users.urls')),

]
