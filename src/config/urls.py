from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('grappelli/', include('grappelli.urls')),  # grappelli URLS
                  path('api/', include('app.internal.urls')),
                  path("admin/", admin.site.urls),
                  # path('api/', include('app.internal.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'app.errors.handler404'
