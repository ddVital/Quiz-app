from django.contrib import admin
from .models import Answer, Notification, Question, Quiz, Result, User

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
# admin.site.register(Answer)

admin.site.register(User)
admin.site.register(Quiz)
# admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Notification)
admin.site.register(Result)