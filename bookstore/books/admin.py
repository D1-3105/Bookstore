from django.contrib import admin
from .models import Books, Authors, Reviews2Books, Reviews2Authors
admin.site.register(Books)
admin.site.register(Authors)
admin.site.register(Reviews2Books)
admin.site.register(Reviews2Authors)
# Register your models here.
