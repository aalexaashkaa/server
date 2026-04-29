from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/ads/', include('apps.ads.urls')),
    path('api/v1/wishlist/', include('apps.wishlist.urls')),
    path('api/v1/exchanges/', include('apps.exchanges.urls')),
    #path('api/v1/', include('apps.notifications.urls')),
    #path('api/v1/', include('apps.preferences.urls')),
    #path('api/v1/', include('apps.recommendations.urls')),
    #path('api/v1/', include('apps.users.urls')),
    #path('api/v1/', include('apps.wishlist.urls')),
    
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)