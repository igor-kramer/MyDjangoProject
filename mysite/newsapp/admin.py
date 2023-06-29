from django.contrib import admin
from newsapp.models import News, Housing, HousingType, NumberOfRooms


class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'text']


class HousingTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'info']


class NumberOfRoomsAdmin(admin.ModelAdmin):
    list_display = ['quantity']


class HousingAdmin(admin.ModelAdmin):
    list_display = ['housing_type', 'number_of_room', 'address', 'square']


admin.site.register(News, NewsAdmin)
admin.site.register(HousingType, HousingTypeAdmin)
admin.site.register(NumberOfRooms, NumberOfRoomsAdmin)
admin.site.register(Housing, HousingAdmin)
