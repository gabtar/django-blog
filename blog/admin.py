from django.contrib import admin
from blog.models import User, Post, Comment

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(User)
