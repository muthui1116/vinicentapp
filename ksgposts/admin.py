from django.contrib import admin
from .models import Post, ReviewRating

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'sub_topic', 'category', 'created_at', 'modified_at')
    prepopulated_fields = {'slug': ('topic',)}

admin.site.register(Post, PostAdmin)
admin.site.register(ReviewRating)
