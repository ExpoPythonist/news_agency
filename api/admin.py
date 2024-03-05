from django.contrib import admin

from api.models import User, NewsStory,Agency


admin.site.register(User)
admin.site.register(NewsStory)
admin.site.register(Agency)
