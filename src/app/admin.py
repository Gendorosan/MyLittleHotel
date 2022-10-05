from django.contrib import admin
from .models import Client,Room,Reserved
# from app.internal.admin.admin_user import AdminUserAdmin

admin.site.site_title = "MyLittleHotel"
admin.site.site_header = "MyLittleHotel"

admin.site.register(Client)
admin.site.register(Room)
admin.site.register(Reserved)