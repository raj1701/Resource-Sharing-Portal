from django.contrib import admin
from .models import Department, Course, Uploader, Resource, Comment, Request


admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Uploader)
admin.site.register(Resource)
admin.site.register(Comment)
admin.site.register(Request)
