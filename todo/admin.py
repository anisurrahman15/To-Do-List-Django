from django.contrib import admin
from .models import Todo

# Register your models here.

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'Last_Modified',) # This line of code will show information from model to admin interface.
    # upper variable cannot ber renamed!


admin.site.register(Todo, TodoAdmin)

