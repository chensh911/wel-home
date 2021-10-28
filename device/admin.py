from django.contrib import admin

# Register your models here.
# Register your models here.
from device.models import Category


class CategoryType(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Category, CategoryType)
