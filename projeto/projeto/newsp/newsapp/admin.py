from django.contrib import admin
from newsapp.models import News, Comment, Category, Profile

class AdminNews(admin.ModelAdmin):
    list_display=('title','category','add_time')
admin.site.register(News,AdminNews)

class AdminComment(admin.ModelAdmin):
    list_display=('news','email','comment','status')
admin.site.register(Comment,AdminComment) 

class AdminCategory(admin.ModelAdmin):
    list_display = ('title', 'category_image')
admin.site.register(Category, AdminCategory)

admin.site.register(Profile)