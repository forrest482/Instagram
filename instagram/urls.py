from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(settings.ADMIN_PATH, admin.site.urls),
    path('activities/', include('activities.urls')),
    path('content/', include('content.urls')),
    path('direct/', include('direct.urls')),
    path('logs/', include('logs.urls')),
    path('users/', include('users.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('api-auth/', include('rest_framework.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
