from django.contrib import admin
from scorecard.models import Course, Lecturer

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'lecturer')

admin.site.register(Course, CourseAdmin)
admin.site.register(Lecturer)