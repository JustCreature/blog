from django.contrib import admin
from .models import Post, Category

# Register your models here.

admin.site.register(Post)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', )
