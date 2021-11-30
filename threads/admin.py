from django.contrib import admin
from .models import Thread, Photo

class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    
  
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Photo)