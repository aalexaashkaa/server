from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/v1/', include('apps.ads.urls')),
    #path('api/v1/', include('apps.books.urls')),
    #path('api/v1/', include('apps.exchanges.urls')),
    #path('api/v1/', include('apps.notifications.urls')),
    #path('api/v1/', include('apps.preferences.urls')),
    #path('api/v1/', include('apps.recommendations.urls')),
    #path('api/v1/', include('apps.users.urls')),
    #path('api/v1/', include('apps.wishlist.urls')),
    #path('api/v1/', include('apps.accounts.urls')),
]