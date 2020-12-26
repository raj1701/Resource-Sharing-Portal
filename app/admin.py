from django.contrib import admin
from .models import Department, Course, Uploader, Resource, Comment, Request, Request_res


admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Uploader)
admin.site.register(Resource)
admin.site.register(Comment)
admin.site.register(Request)
admin.site.register(Request_res)
