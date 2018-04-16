from django.contrib import admin

from seleniumtest.models import Question, Choice

admin.site.register(Question)
admin.site.register(Choice)
