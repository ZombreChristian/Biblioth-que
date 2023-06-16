from django.contrib import admin

from bookstore.models import Book, CustomUser

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Book)
