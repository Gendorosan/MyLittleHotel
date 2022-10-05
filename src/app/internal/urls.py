from django.urls import path
from .. import handlers

urlpatterns = [
                  path('', handlers.test, name='test'),
                  #path('<int:room_id>', handlers.details, name='details'),
                  #path('api/', include('app.internal.urls')),
              ]

